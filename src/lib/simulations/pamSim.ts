import { browser } from "$app/environment";
import { base } from "$app/paths";
import type { ProtocolStep } from "@computational-biology-aachen/mxlweb-core/pam";

import { initModel } from "$lib/simulations/matuszynska2016_npq";
import type {
  SimulationRequest,
  SimulationResult,
} from "@computational-biology-aachen/mxlweb-core";

import wasmWorkerUrlString from "@computational-biology-aachen/mxlweb-core/backends/wasm/wasmWorker.ts?worker&url";

export const LOG_STEPS = [
  1, 2, 3, 4, 6, 10, 16, 25, 40, 63, 100, 158, 251, 398, 631, 1000, 1585, 2512,
  3981, 6310, 10000,
];

export interface SimParams {
  AL: number;
  SP: number;
  CtZ: number;
  CtV: number;
}

let worker: Worker | null = null;
const handlers = new Set<(data: SimulationResult) => void>();

if (browser) {
  const url = new URL(wasmWorkerUrlString, import.meta.url);
  worker = new Worker(url, { type: "module" });
  worker.postMessage({ type: "__INIT__", basePath: base });
  worker.onmessage = (e: MessageEvent<SimulationResult>) =>
    handlers.forEach((h) => h(e.data));
}

function nextId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

// Build the model once: all simulations share the same compiled WAT + derived
// fns. Everything below is snapshotted into plain values so simulate() never
// touches the reactive ModelBuilder (its SvelteMaps would otherwise create a
// dependency loop when called inside a Svelte $effect).
const model = initModel();
const rhsWat = model.buildWat();
const { allDerived, selectDerived } = model.buildJsDerived(["Fluo"]);
const paramNames = model.getParameterNames();
const order = model.sortDependencies();
const rhsNames = model.getNames();
const initialValues = model.resolveInitialValues();
const baseParams = model.resolveParameters();
const idxDV = paramNames.indexOf("k_DV");
const idxEZ = paramNames.indexOf("k_EZ");

/**
 * Run one PAM simulation on the shared worker. Resolves with the result whose
 * requestId matches this call; rejects on solver/worker error.
 */
export function simulate(
  protocol: ProtocolStep[],
  kDeepoxV: number,
  kEpoxZ: number,
): Promise<SimulationResult> {
  if (!worker) return Promise.reject(new Error("Worker unavailable (SSR)"));
  const pars = baseParams.slice();
  if (idxDV >= 0) pars[idxDV] = kDeepoxV;
  if (idxEZ >= 0) pars[idxEZ] = kEpoxZ;

  const id = nextId();
  const request: SimulationRequest = {
    requestId: id,
    rhsWat,
    allDerivedFn: allDerived,
    selectDerivedFn: selectDerived,
    initialValues,
    rhsNames,
    allDerivedNames: order,
    selectDerivedNames: ["Fluo"],
    tEnd: 0,
    nTimePoints: 500,
    pars,
    parNames: paramNames,
    method: "radau5",
    calculateDerived: true,
    protocol,
    rtol: 1e-8,
    atol: 1e-8,
  };

  return new Promise((resolve, reject) => {
    const handler = (data: SimulationResult) => {
      if (data.requestId !== id) return;
      handlers.delete(handler);
      if (data.err) reject(new Error(data.err.message));
      else resolve(data);
    };
    handlers.add(handler);
    worker!.postMessage(request);
  });
}
