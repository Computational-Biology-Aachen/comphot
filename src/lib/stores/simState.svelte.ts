import { WorkerManager, simWorker, type Res, type SimRequest } from './workerStore';

export interface SimParams {
	AL: number;
	SP: number;
	CtZ: number;
	CtV: number;
}

/** np.round(np.logspace(0, 4, 21)) */
export const LOG_STEPS = [
	1, 2, 3, 4, 6, 10, 16, 25, 40, 63, 100, 158, 251, 398, 631, 1000, 1585, 2512, 3981, 6310, 10000
];

/**
 * Reactive simulation state. Instantiate once per page, then call `setup()`
 * during component initialization to wire up worker subscriptions.
 */
export class SimState {
	currentResult = $state<Res | null>(null);
	previousResult = $state<Res | null>(null);
	currentParams = $state<SimParams | null>(null);
	previousParams = $state<SimParams | null>(null);
	loading = $state(false);
	errorMsg = $state('');

	#pendingParams: SimParams | null = null;
	#pendingRequestId: string | null = null;

	/** Must be called during component initialization (top-level script, not inside callbacks). */
	setup() {
		$effect(() => {
			const unsubMsg = simWorker.onMessage((data) => {
				if (data.requestId !== this.#pendingRequestId) return;
				this.loading = false;
				this.#pendingRequestId = null;
				if (data.message) {
					this.errorMsg = `Simulation error: ${data.message}`;
					return;
				}
				this.errorMsg = '';
				this.previousResult = this.currentResult;
				this.previousParams = this.currentParams;
				this.currentResult = data.res;
				this.currentParams = this.#pendingParams;
				this.#pendingParams = null;
			});
			const unsubErr = simWorker.onError(() => {
				this.loading = false;
				this.#pendingRequestId = null;
				this.errorMsg = 'Worker error — see browser console for details.';
			});
			return () => {
				unsubMsg();
				unsubErr();
			};
		});
	}

	run(protocol: SimRequest['protocol'], params: SimParams, pars: number[]) {
		if (this.loading) return;
		const requestId = WorkerManager.generateRequestId();
		this.#pendingRequestId = requestId;
		this.loading = true;
		this.errorMsg = '';
		this.#pendingParams = params;
		simWorker.postMessage({ requestId, protocol, pars });
	}
}
