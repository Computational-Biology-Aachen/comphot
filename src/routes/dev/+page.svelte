<script lang="ts">
	import CompareCheckbox from '$lib/components/simulation/CompareCheckbox.svelte';
	import LineChart from '$lib/components/simulation/LineChart.svelte';
	import ParameterTable from '$lib/components/simulation/ParameterTable.svelte';
	import RunButton from '$lib/components/simulation/RunButton.svelte';
	import type { PhaseRegion } from '$lib/components/simulation/SimChart.svelte';
	import { ta } from '$lib/i18n';
	import * as m from '$lib/paraglide/messages';
	import { buildPamProtocol } from '$lib/simulations/pam';
	import { audienceStore } from '$lib/stores/audience.svelte';
	import { WorkerManager, simWorker, type Res } from '$lib/stores/workerStore';
	import { onDestroy, onMount } from 'svelte';

	interface SimParams {
		AL: number;
		SP: number;
		CtZ: number;
		CtV: number;
	}

	// Logspace steps: np.round(np.logspace(0, 4, 21))
	const LOG_STEPS = [
		1, 2, 3, 4, 6, 10, 16, 25, 40, 63, 100, 158, 251, 398, 631, 1000, 1585, 2512, 3981, 6310, 10000
	];

	// Slider state
	let lightIntensity = $state(100);
	let totalMinutes = $state(1);
	let pulseInterval = $state(85);
	let darkLength = $state(30);
	let saturatingPulse = $state(5000);

	let compareWithLast = $state(true);
	let showAnswers = $state(false);

	// Derived slider values
	let activationIdx = $state(10); // LOG_STEPS[10] = 100
	let deactivationIdx = $state(10);
	const activationMultiplier = $derived(LOG_STEPS[activationIdx]);
	const deactivationMultiplier = $derived(LOG_STEPS[deactivationIdx]);
	const totalTime = $derived(totalMinutes * 60);

	// Simulation state
	let currentResult = $state<Res | null>(null);
	let previousResult = $state<Res | null>(null);
	let currentParams = $state<SimParams | null>(null);
	let previousParams = $state<SimParams | null>(null);
	let pendingParams = $state<SimParams | null>(null);
	let loading = $state(false);
	let errorMsg = $state('');
	let pendingRequestId: string | null = null;

	// Worker subscriptions
	let unsubMessage: (() => void) | null = null;
	let unsubError: (() => void) | null = null;

	onMount(() => {
		unsubMessage = simWorker.onMessage((data) => {
			if (data.requestId !== pendingRequestId) return;
			loading = false;
			pendingRequestId = null;

			if (data.message) {
				errorMsg = data.message ? `Simulation error: ${data.message}` : 'Empty result.';
				return;
			}
			errorMsg = '';
			// Shift current → previous, apply new
			previousResult = currentResult;
			previousParams = currentParams;
			currentResult = data.res;
			currentParams = pendingParams;
			pendingParams = null;
		});

		unsubError = simWorker.onError(() => {
			loading = false;
			pendingRequestId = null;
			errorMsg = 'Worker error — see browser console for details.';
		});

		runSimulation();
	});

	onDestroy(() => {
		unsubMessage?.();
		unsubError?.();
	});

	// Run simulation
	function runSimulation() {
		if (loading) return;

		const protocol = buildPamProtocol({
			lightIntensity,
			saturatingPulse: saturatingPulse,
			totalMinutes,
			darkLength: darkLength,
			pulseInterval
		});

		const requestId = WorkerManager.generateRequestId();
		pendingRequestId = requestId;
		loading = true;
		errorMsg = '';

		const kDeepoxV = 0.0024 * (activationMultiplier / 100);
		const kEpoxZ = 0.00024 * (deactivationMultiplier / 100);

		pendingParams = { AL: lightIntensity, SP: saturatingPulse, CtZ: kDeepoxV, CtV: kEpoxZ };

		simWorker.postMessage({
			requestId,
			protocol,
			pars: [kDeepoxV, kEpoxZ]
		});
	}

	// Phase background regions
	const phases = $derived.by<PhaseRegion[]>(() => {
		const dl = darkLength;
		const maxT = totalMinutes * 60;
		return [
			{ start: 0, end: dl, color: 'rgba(28, 91, 199, 0.18)' },
			{ start: dl, end: maxT, color: 'rgba(207, 109, 12, 0.18)' }
		];
	});

	// Derived display
	const showOld = $derived(compareWithLast && previousResult !== null);

	const paramRows = $derived.by(() => {
		if (!currentParams) return [];
		return [
			{ label: 'AL [μmol m⁻² s⁻¹]', newVal: currentParams.AL, oldVal: previousParams?.AL },
			{ label: 'SP [μmol m⁻² s⁻¹]', newVal: currentParams.SP, oldVal: previousParams?.SP },
			{
				label: 'CtZ [s⁻¹]',
				newVal: currentParams.CtZ.toFixed(5),
				oldVal: previousParams?.CtZ?.toFixed(5)
			},
			{
				label: 'CtV [s⁻¹]',
				newVal: currentParams.CtV.toFixed(6),
				oldVal: previousParams?.CtV?.toFixed(6)
			}
		];
	});

	let lineData = $derived.by(() => {
		if (previousResult !== null) {
			return {
				labels: currentResult?.time,
				datasets: [
					{
						label: 'new',
						data: currentResult?.fluo,
						borderColor: '#FF4B4B',
						backgroundColor: '#FF4B4B'
					},
					{
						label: 'old',
						data: previousResult?.fluo,
						borderColor: '#FF4B4B',
						backgroundColor: '#FF4B4B',
						borderDash: [6, 3]
					}
				]
			};
		}
		return {
			labels: currentResult?.time,
			datasets: [
				{
					label: 'fluo',
					data: currentResult?.fluo,
					borderColor: '#FF4B4B',
					backgroundColor: '#FF4B4B'
				}
			]
		};
	});
	let npqData = $derived.by(() => {
		if (previousResult !== null) {
			return {
				labels: currentResult?.npqTime,
				datasets: [
					{
						label: 'new',
						data: currentResult?.npq,
						borderColor: '#FF4B4B',
						backgroundColor: '#FF4B4B'
					},
					{
						label: 'old',
						data: previousResult?.npq,
						borderColor: '#FF4B4B',
						backgroundColor: '#FF4B4B',
						borderDash: [6, 3]
					}
				]
			};
		}
		return {
			labels: currentResult?.npqTime,
			datasets: [
				{
					label: 'NPQ',
					data: currentResult?.npq,
					borderColor: '#FF4B4B',
					backgroundColor: '#FF4B4B'
				}
			]
		};
	});
	let psiiData = $derived.by(() => {
		console.log('Updated');
		console.log($state.snapshot(currentResult?.phiPsii));
		if (previousResult !== null) {
			return {
				labels: currentResult?.npqTime,
				datasets: [
					{
						label: 'new',
						data: currentResult?.phiPsii,
						borderColor: '#FF4B4B',
						backgroundColor: '#FF4B4B'
					},
					{
						label: 'old',
						data: previousResult?.phiPsii,
						borderColor: '#FF4B4B',
						backgroundColor: '#FF4B4B',
						borderDash: [6, 3]
					}
				]
			};
		}
		return {
			labels: currentResult?.npqTime,
			datasets: [
				{
					label: 'phi(PSII)',
					data: currentResult?.phiPsii,
					borderColor: '#FF4B4B',
					backgroundColor: '#FF4B4B'
				}
			]
		};
	});
</script>

<svelte:head>
	<title>Dev</title>
</svelte:head>

<!-- Slider controls -------------------------------- -->
<div class="slider-section">
	<label class="slider-label">
		{@html m.slider_light()}: <strong>{lightIntensity}</strong>
		<input type="range" min="50" max="900" step="50" bind:value={lightIntensity} />
	</label>

	<div class="slider-row">
		<label class="slider-label">
			{@html m.fal_slider_time()}: <strong>{totalMinutes} min</strong>
			<input type="range" min="1" max="15" step="1" bind:value={totalMinutes} />
		</label>
		<label class="slider-label">
			{@html m.slider_pulses()}: <strong>{pulseInterval} s</strong>
			<input type="range" min="5" max="150" step="5" bind:value={pulseInterval} />
		</label>
	</div>

	{#if audienceStore.audience === '4bio'}
		<div class="slider-row">
			<div class="slider-col">
				<label class="slider-label">
					{@html m.slider_activation()}: <strong>{activationMultiplier}</strong>
					<input type="range" min="0" max="20" step="1" bind:value={activationIdx} />
				</label>
				<label class="slider-label">
					{@html m.fal_slider_darklength()}: <strong>{darkLength} s</strong>
					<input type="range" min="0" max={totalMinutes * 60} step="5" bind:value={darkLength} />
				</label>
			</div>
			<div class="slider-col">
				<label class="slider-label">
					{@html m.slider_deactivation()}: <strong>{deactivationMultiplier}</strong>
					<input type="range" min="0" max="20" step="1" bind:value={deactivationIdx} />
				</label>
				<label class="slider-label">
					{@html m.fal_slider_saturate()}: <strong>{saturatingPulse}</strong>
					<input type="range" min="0" max="10000" step="500" bind:value={saturatingPulse} />
				</label>
			</div>
		</div>
	{/if}
</div>

<!-- Run controls -->
<div class="run-controls">
	<div class="run-btn-wrap">
		<RunButton {loading} onclick={runSimulation} />
	</div>
	<CompareCheckbox bind:checked={compareWithLast} />
</div>

{#if errorMsg}
	<p class="error-msg">{errorMsg}</p>
{/if}

<!-- Results ---------------------------------------- -->
{#if currentResult}
	<div class="charts-section">
		<div class="charts-grid">
			<div class="chart-card">
				<p class="chart-label">{ta(m.bio_fluo(), m.math_fluo())}</p>
				<LineChart data={lineData} loading={false} {phases} yMax={1.2} />
			</div>

			<div class="chart-card">
				<p class="chart-label">{m.axis_npq()}</p>
				<LineChart data={npqData} loading={false} />
			</div>

			<div class="chart-card">
				<p class="chart-label">{m.axis_phipsii()}</p>
				<LineChart data={psiiData} loading={false} />
			</div>
		</div>

		{#if paramRows.length > 0}
			<div class="param-table-wrap">
				<ParameterTable
					rows={paramRows}
					showOld={showOld && previousParams !== null}
					newLabel={m.new_label()}
					oldLabel={m.old_label()}
				/>
			</div>
		{/if}
	</div>
{/if}

<style>
	.prose :global(h1),
	.prose :global(h2),
	.prose :global(h3),
	.prose :global(h4),
	.prose :global(h5) {
		margin-top: var(--space-5);
		margin-bottom: var(--space-2);
		line-height: 1.3;
	}

	.prose :global(p) {
		margin-bottom: var(--space-3);
	}

	.fig {
		margin: var(--space-6) auto;
		text-align: center;
		max-width: 80%;
	}

	.fig img {
		max-width: 100%;
		border-radius: 6px;
	}

	.fig figcaption {
		font-size: 0.85rem;
		color: var(--color-text-muted);
		margin-top: var(--space-2);
	}

	.math-block {
		overflow-x: auto;
		margin: var(--space-4) 0;
	}

	.math-inline {
		margin: var(--space-3) 0;
	}

	pre {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 6px;
		padding: var(--space-4);
		overflow-x: auto;
		font-size: 0.82rem;
		line-height: 1.5;
		margin: var(--space-3) 0;
	}

	code {
		font-family: var(--font-mono);
	}

	details {
		margin: var(--space-2) 0;
		border: 1px solid var(--color-border);
		border-radius: 6px;
	}

	details summary {
		padding: var(--space-2) var(--space-3);
		cursor: pointer;
		font-weight: 500;
		font-size: 0.9rem;
		background: var(--color-surface);
		border-radius: 6px;
	}

	details[open] summary {
		border-radius: 6px 6px 0 0;
	}

	details[open] pre {
		border-radius: 0 0 6px 6px;
		border-top: 1px solid var(--color-border);
		margin: 0;
	}

	.toggle-label {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		cursor: pointer;
		margin-bottom: var(--space-3);
		font-size: 0.95rem;
	}

	.toggle-label input {
		accent-color: var(--color-primary);
		width: 1.1em;
		height: 1.1em;
	}

	.qa-text :global(ul) {
		padding-left: 1.5rem;
	}

	.slider-section {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 8px;
		padding: var(--space-4);
		margin: var(--space-4) 0;
		display: flex;
		flex-direction: column;
		gap: var(--space-4);
	}

	.slider-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--space-4);
	}

	.slider-col {
		display: flex;
		flex-direction: column;
		gap: var(--space-3);
	}

	.slider-label {
		display: flex;
		flex-direction: column;
		gap: var(--space-1);
		font-size: 0.88rem;
	}

	.slider-label input[type='range'] {
		width: 100%;
		accent-color: var(--color-primary);
		cursor: pointer;
		margin-top: 2px;
	}

	.run-controls {
		display: flex;
		align-items: center;
		gap: var(--space-4);
		margin: var(--space-4) 0;
	}

	.run-btn-wrap {
		width: 220px;
		flex-shrink: 0;
	}

	.error-msg {
		color: #c0392b;
		background: #fdf0f0;
		border: 1px solid #f5c6cb;
		border-radius: 6px;
		padding: var(--space-3);
		margin: var(--space-3) 0;
	}

	.charts-section {
		margin: var(--space-6) 0;
	}

	.charts-grid {
		display: grid;
		grid-template-columns: 1fr;
		gap: var(--space-4);
		max-width: 600px;
	}

	.charts-grid.three-cols {
		grid-template-columns: repeat(3, 1fr);
		max-width: unset;
	}

	.chart-card {
		border: 1px solid var(--color-border);
		border-radius: 8px;
		padding: var(--space-3);
		background: var(--color-bg);
	}

	.chart-label {
		margin: 0 0 var(--space-2) 0;
		font-size: 0.85rem;
		font-weight: 500;
		color: var(--color-text-muted);
	}

	.param-table-wrap {
		margin-top: var(--space-4);
		max-width: 440px;
	}

	@media (max-width: 750px) {
		.charts-grid.three-cols {
			grid-template-columns: 1fr;
		}

		.slider-row {
			grid-template-columns: 1fr;
		}

		.run-controls {
			flex-direction: column;
			align-items: flex-start;
		}

		.run-btn-wrap {
			width: 100%;
		}
	}
</style>
