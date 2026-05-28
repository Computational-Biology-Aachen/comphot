import { browser } from '$app/environment';
import { base } from '$app/paths';
import type { SimulationRequest, SimulationResult } from '@computational-biology-aachen/mxlweb-core';
import type { ProtocolStep } from '$lib/simulations/pam';
import { initModel } from '$lib/simulations/pamModel';

import wasmWorkerUrlString from '@computational-biology-aachen/mxlweb-core/backends/wasm/wasmWorker.ts?worker&url';

export const LOG_STEPS = [
	1, 2, 3, 4, 6, 10, 16, 25, 40, 63, 100, 158, 251, 398, 631, 1000, 1585, 2512, 3981, 6310, 10000
];

export interface SimParams {
	AL: number;
	SP: number;
	CtZ: number;
	CtV: number;
}

class WorkerManager {
	private worker: Worker | null = null;
	private messageHandlers = new Set<(data: SimulationResult) => void>();
	private errorHandlers = new Set<(e: ErrorEvent) => void>();

	constructor(url: URL) {
		if (browser) {
			this.worker = new Worker(url, { type: 'module' });
			this.worker.postMessage({ type: '__INIT__', basePath: base });
			this.worker.onmessage = (e: MessageEvent<SimulationResult>) => {
				this.messageHandlers.forEach((h) => h(e.data));
			};
			this.worker.onerror = (e: ErrorEvent) => {
				this.errorHandlers.forEach((h) => h(e));
			};
		}
	}

	onMessage(handler: (data: SimulationResult) => void): () => void {
		this.messageHandlers.add(handler);
		return () => this.messageHandlers.delete(handler);
	}

	onError(handler: (e: ErrorEvent) => void): () => void {
		this.errorHandlers.add(handler);
		return () => this.errorHandlers.delete(handler);
	}

	postMessage(req: SimulationRequest): void {
		this.worker?.postMessage(req);
	}

	static generateId(): string {
		return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
	}
}

const wasmWorkerUrl = browser
	? new URL(wasmWorkerUrlString, import.meta.url)
	: new URL('http://localhost');

const simWorker = new WorkerManager(wasmWorkerUrl);

export class SimState {
	currentResult = $state<SimulationResult | null>(null);
	previousResult = $state<SimulationResult | null>(null);
	currentParams = $state<SimParams | null>(null);
	previousParams = $state<SimParams | null>(null);
	loading = $state(false);
	errorMsg = $state('');

	readonly #model = initModel();
	readonly #rhsWat: string;
	readonly #allDerivedFn: string;
	readonly #selectDerivedFn: string;
	readonly #paramNames: string[];
	readonly #order: string[];

	#pendingParams: SimParams | null = null;
	#pendingId: string | null = null;

	constructor() {
		this.#rhsWat = this.#model.buildWat();
		const { allDerived, selectDerived } = this.#model.buildJsDerived(['Fluo']);
		this.#allDerivedFn = allDerived;
		this.#selectDerivedFn = selectDerived;
		this.#paramNames = this.#model.getParameterNames();
		this.#order = this.#model.sortDependencies();
	}

	setup() {
		$effect(() => {
			const unsubMsg = simWorker.onMessage((data) => {
				if (data.requestId !== this.#pendingId) return;
				this.loading = false;
				this.#pendingId = null;
				if (data.err) {
					this.errorMsg = `Simulation error: ${data.err.message}`;
					return;
				}
				this.errorMsg = '';
				this.previousResult = this.currentResult;
				this.previousParams = this.currentParams;
				this.currentResult = data;
				this.currentParams = this.#pendingParams;
				this.#pendingParams = null;
			});
			const unsubErr = simWorker.onError(() => {
				this.loading = false;
				this.#pendingId = null;
				this.errorMsg = 'Worker error — see browser console for details.';
			});
			return () => {
				unsubMsg();
				unsubErr();
			};
		});
	}

	run(protocol: ProtocolStep[], params: SimParams, kDeepoxV: number, kEpoxZ: number) {
		if (this.loading) return;
		this.#model.updateParameter('kf_violaxanthin_deepoxidase', { value: kDeepoxV });
		this.#model.updateParameter('kf_zeaxanthin_epoxidase', { value: kEpoxZ });

		const id = WorkerManager.generateId();
		this.#pendingId = id;
		this.#pendingParams = params;
		this.loading = true;
		this.errorMsg = '';

		simWorker.postMessage({
			requestId: id,
			rhsWat: this.#rhsWat,
			allDerivedFn: this.#allDerivedFn,
			selectDerivedFn: this.#selectDerivedFn,
			initialValues: this.#model.resolveInitialValues(),
			rhsNames: this.#model.getNames(),
			allDerivedNames: this.#order,
			selectDerivedNames: ['Fluo'],
			tEnd: 0,
			nTimePoints: 100,
			pars: this.#model.resolveParameters(),
			parNames: this.#paramNames,
			method: 'radau5',
			calculateDerived: true,
			protocol
		});
	}
}
