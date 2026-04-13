import type { Res, SimRequest, WorkerMessage } from '$lib/stores/workerStore';
import { loadPyodide, version } from 'pyodide';
export {}; // make it a module

let pyodideReady = false;
let pyFuncs: any; // eslint-disable-line @typescript-eslint/no-explicit-any
let basePath = ''; // Set via __INIT__ message
let pyodidePromise: Promise<any> | null = null; // eslint-disable-line @typescript-eslint/no-explicit-any

const indexURL = `https://cdn.jsdelivr.net/pyodide/v${version}/full/`;

async function setupPyodide() {
	try {
		const pyodide = await loadPyodide({
			indexURL,
			packages: ['numpy', 'scipy', 'pandas']
		});

		const response = await fetch(`${basePath}/main.py`);
		if (!response.ok) {
			throw new Error(`Failed to fetch main.py: ${response.status} ${response.statusText}`);
		}
		const pythonScript = await response.text();
		pyFuncs = pyodide.runPython(pythonScript);
		pyodideReady = true;
		return pyodide;
	} catch (e) {
		console.error('Pyodide loading failed:', e);
	}
}

onmessage = async function (event: MessageEvent) {
	if (event.data.type === '__INIT__') {
		basePath = event.data.basePath ?? '';
		pyodidePromise = setupPyodide();
		return;
	}

	const pyodide = await pyodidePromise;

	if (!pyodideReady || !pyodide) {
		postMessage({ message: 'pyodide_not_available', requestId: event.data.requestId });
		return;
	}

	const { requestId, protocol, pars }: SimRequest = event.data;

	try {
		const [resPy, errPy] = pyFuncs.integrate(pyodide.toPy(protocol), pyodide.toPy(pars));

		const res: Res = resPy.toJs();
		const errStr: string | undefined = errPy ?? undefined;

		const message: WorkerMessage = {
			requestId,
			res,
			message: errStr
		};
		postMessage(message);
	} catch (e) {
		const message: WorkerMessage = {
			requestId,
			res: {
				time: [],
				atp: [],
				pqOx: [],
				pcOx: [],
				fdOx: [],
				hLumen: [],
				psbsDe: [],
				lhc: [],
				vX: [],
				fluo: [],
				npqTime: [],
				npq: [],
				phiPsii: []
			},
			message: String(e)
		};
		postMessage(message);
	}
};
