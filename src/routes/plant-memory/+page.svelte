<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { marked } from 'marked';
	import { base } from '$app/paths';
	import { t } from '$lib/i18n';
	import { audienceStore } from '$lib/stores/audience.svelte';
	import { WorkerManager, simWorker } from '$lib/stores/workerStore';
	import { buildMemoryProtocol } from '$lib/simulations/pam';
	import { processResults } from '$lib/simulations/processResults';
	import { NPQ_Y0 } from '$lib/simulations/initialValues';
	import PageNav from '$lib/components/PageNav.svelte';
	import Expander from '$lib/components/Expander.svelte';
	import InfoBox from '$lib/components/InfoBox.svelte';
	import SimChart from '$lib/components/simulation/SimChart.svelte';
	import RunButton from '$lib/components/simulation/RunButton.svelte';
	import CompareCheckbox from '$lib/components/simulation/CompareCheckbox.svelte';
	import ParameterTable from '$lib/components/simulation/ParameterTable.svelte';
	import type { PhaseRegion } from '$lib/components/simulation/SimChart.svelte';

	// ── Logspace steps (same as experiments page)
	const LOG_STEPS = [
		1, 2, 3, 4, 6, 10, 16, 25, 40, 63, 100, 158, 251, 398, 631, 1000, 1585, 2512, 3981, 6310,
		10000
	];

	// ── Slider state
	let lightIntensity = $state(100);
	let pulseInterval = $state(85);
	let darkLength = $state(30);
	let saturatingPulse = $state(5000);
	let trainingLength = $state(300); // 5 min default → spec says 300s
	let relaxationLength = $state(300);
	let memoryLength = $state(300);

	// 4bio only
	let activationIdx = $state(10); // LOG_STEPS[10] = 100
	let deactivationIdx = $state(10);

	let compareWithLast = $state(true);
	let showAnswers = $state(false);

	// ── Derived
	const activationMultiplier = $derived(LOG_STEPS[activationIdx]);
	const deactivationMultiplier = $derived(LOG_STEPS[deactivationIdx]);
	const totalTime = $derived(darkLength + trainingLength + relaxationLength + memoryLength);

	// ── Simulation types
	type SimResult = ReturnType<typeof processResults>;
	interface SimParams {
		AL: number;
		SP: number;
		CtZ: number;
		CtV: number;
	}

	// ── Simulation state
	let currentResult = $state<SimResult | null>(null);
	let previousResult = $state<SimResult | null>(null);
	let currentParams = $state<SimParams | null>(null);
	let previousParams = $state<SimParams | null>(null);
	let pendingParams = $state<SimParams | null>(null);
	let loading = $state(false);
	let errorMsg = $state('');
	let pendingRequestId: string | null = null;

	// ── Worker subscriptions
	let unsubMessage: (() => void) | null = null;
	let unsubError: (() => void) | null = null;

	onMount(() => {
		unsubMessage = simWorker.onMessage((data) => {
			if (data.requestId !== pendingRequestId) return;
			loading = false;
			pendingRequestId = null;

			if (!data.time.length) {
				errorMsg = data.message ? `Simulation error: ${data.message}` : 'Empty result.';
				return;
			}
			errorMsg = '';
			const processed = processResults(data.time, data.values);
			previousResult = currentResult;
			previousParams = currentParams;
			currentResult = processed;
			currentParams = pendingParams;
			pendingParams = null;
		});

		unsubError = simWorker.onError(() => {
			loading = false;
			pendingRequestId = null;
			errorMsg = 'Worker error — see browser console for details.';
		});
	});

	onDestroy(() => {
		unsubMessage?.();
		unsubError?.();
	});

	// ── Run simulation
	function runSimulation() {
		if (loading) return;
		const isMath = audienceStore.audience === '4math';
		const kDeepoxV = isMath ? 0.0024 : 0.0024 * (activationMultiplier / 100);
		const kEpoxZ = isMath ? 0.00024 : 0.00024 * (deactivationMultiplier / 100);

		const protocol = buildMemoryProtocol({
			lightIntensity,
			saturatingPulse,
			darkLength,
			pulseInterval,
			trainingLength,
			relaxationLength,
			memoryLength
		});

		pendingParams = { AL: lightIntensity, SP: saturatingPulse, CtZ: kDeepoxV, CtV: kEpoxZ };
		const requestId = WorkerManager.generateRequestId();
		pendingRequestId = requestId;
		loading = true;
		errorMsg = '';

		simWorker.postMessage({
			requestId,
			protocol,
			y0: NPQ_Y0,
			parsOverride: { kDeepoxV, kEpoxZ }
		});
	}

	// ── Phase regions for 4-phase memory protocol
	const phases = $derived.by<PhaseRegion[]>(() => {
		const trainStart = darkLength;
		const relaxStart = trainStart + trainingLength;
		const memStart = relaxStart + relaxationLength;
		const end = memStart + memoryLength;
		const regions: PhaseRegion[] = [];

		if (darkLength > 0) {
			regions.push({
				start: 0,
				end: trainStart,
				color: 'rgba(28, 91, 199, 0.25)',
				label: ''
			});
		}
		if (trainingLength > 0) {
			regions.push({
				start: trainStart,
				end: relaxStart,
				color: 'rgba(207, 109, 12, 0.25)',
				label: t('mem_anno_training')
			});
		}
		if (relaxationLength > 0) {
			regions.push({
				start: relaxStart,
				end: memStart,
				color: 'rgba(28, 91, 199, 0.25)',
				label: t('mem_anno_relaxation')
			});
		}
		if (memoryLength > 0) {
			regions.push({
				start: memStart,
				end,
				color: 'rgba(209, 10, 13, 0.25)',
				label: t('mem_anno_memory')
			});
		}
		return regions;
	});

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
</script>

<svelte:head>
	<title>Plant Light Memory</title>
</svelte:head>

<h1>{@html marked(t('mem_headline_brain'))}</h1>

<InfoBox>
	{@html marked(t('mem_learning_objectives'))}
</InfoBox>

<PageNav
	prev={{ href: '/experiments', label: 'Experiments in Silico' }}
	next={{ href: '/conclusion', label: 'Conclusion' }}
/>

<!-- ── Explanation ──────────────────────────────────── -->
<div class="intro-content">
	{@html marked(t('mem_introduction_brain'))}
</div>

<figure class="fig">
	<img
		src="{base}/pictures/NPQphotosynthesis.png"
		alt="Memory protocol diagram"
		class="protocol-img"
	/>
	<figcaption>Memory protocol overview</figcaption>
</figure>

<!-- ── Guiding questions ─────────────────────────────── -->
<Expander title={t('mem_guiding_expander')} open>
	<div class="prose">{@html marked(t('mem_guiding_header'))}</div>
	<label class="toggle-label">
		<input type="checkbox" bind:checked={showAnswers} />
		{@html marked.parseInline(t('mem_guiding_toggle'))}
	</label>
	{#if !showAnswers}
		<div class="qa-text">{@html marked(t('mem_guiding_questions'))}</div>
	{:else}
		<div class="qa-text">{@html marked(t('mem_guiding_answers'))}</div>
	{/if}
</Expander>

<!-- ── Sliders ──────────────────────────────────────── -->
<div class="slider-section">
	<!-- Common sliders -->
	<div class="slider-row">
		<label class="slider-label">
			{@html t('slider_light')}: <strong>{lightIntensity}</strong>
			<input type="range" min="50" max="900" step="50" bind:value={lightIntensity} />
		</label>
		<label class="slider-label">
			{@html t('slider_pulses')}: <strong>{pulseInterval} s</strong>
			<input type="range" min="5" max="150" step="5" bind:value={pulseInterval} />
		</label>
	</div>

	<div class="slider-row">
		<label class="slider-label">
			{@html t('fal_slider_darklength')}: <strong>{darkLength} s</strong>
			<input type="range" min="0" max="300" step="10" bind:value={darkLength} />
		</label>
		<label class="slider-label">
			{@html t('fal_slider_saturate')}: <strong>{saturatingPulse}</strong>
			<input type="range" min="0" max="10000" step="500" bind:value={saturatingPulse} />
		</label>
	</div>

	<div class="slider-row three">
		<label class="slider-label">
			{@html t('mem_slider_training')}: <strong>{trainingLength} s</strong>
			<input type="range" min="0" max="600" step="30" bind:value={trainingLength} />
		</label>
		<label class="slider-label">
			{@html t('mem_slider_relaxation')}: <strong>{relaxationLength} s</strong>
			<input type="range" min="0" max="600" step="30" bind:value={relaxationLength} />
		</label>
		<label class="slider-label">
			{@html t('mem_slider_memory')}: <strong>{memoryLength} s</strong>
			<input type="range" min="0" max="600" step="30" bind:value={memoryLength} />
		</label>
	</div>

	<!-- 4bio: activation/deactivation sliders -->
	{#if audienceStore.audience === '4bio'}
		<div class="slider-row">
			<label class="slider-label">
				{@html t('slider_activation')}: <strong>{activationMultiplier}</strong>
				<input type="range" min="0" max="20" step="1" bind:value={activationIdx} />
			</label>
			<label class="slider-label">
				{@html t('slider_deactivation')}: <strong>{deactivationMultiplier}</strong>
				<input type="range" min="0" max="20" step="1" bind:value={deactivationIdx} />
			</label>
		</div>
	{/if}
</div>

<!-- ── Run controls ── -->
<div class="run-controls">
	<div class="run-btn-wrap">
		<RunButton {loading} onclick={runSimulation} />
	</div>
	<CompareCheckbox bind:checked={compareWithLast} />
</div>

{#if errorMsg}
	<p class="error-msg">{errorMsg}</p>
{/if}

<!-- ── Results ──────────────────────────────────────── -->
{#if currentResult}
	<div class="charts-section">
		<div class="charts-grid" class:three-cols={audienceStore.audience === '4bio'}>
			<div class="chart-card">
				<p class="chart-label">{t('fluo')}</p>
				<SimChart
					xNew={currentResult.time}
					yNew={currentResult.fluo}
					xOld={showOld && previousResult ? previousResult.time : []}
					yOld={showOld && previousResult ? previousResult.fluo : []}
					{phases}
					yLabel={t('fluo')}
					showLine={true}
					{totalTime}
				/>
			</div>

			{#if audienceStore.audience === '4bio'}
				<div class="chart-card">
					<p class="chart-label">{t('axis_npq')}</p>
					<SimChart
						xNew={currentResult.npqTime}
						yNew={currentResult.npq}
						xOld={showOld && previousResult ? previousResult.npqTime : []}
						yOld={showOld && previousResult ? previousResult.npq : []}
						{phases}
						yLabel={t('axis_npq')}
						showLine={false}
						{totalTime}
					/>
				</div>

				<div class="chart-card">
					<p class="chart-label">{t('axis_phipsii')}</p>
					<SimChart
						xNew={currentResult.phiTime}
						yNew={currentResult.phiPSII}
						xOld={showOld && previousResult ? previousResult.phiTime : []}
						yOld={showOld && previousResult ? previousResult.phiPSII : []}
						{phases}
						yLabel={t('axis_phipsii')}
						showLine={false}
						{totalTime}
					/>
				</div>
			{/if}
		</div>

		{#if paramRows.length > 0}
			<div class="param-table-wrap">
				<ParameterTable
					rows={paramRows}
					showOld={showOld && previousParams !== null}
					newLabel={t('new_label')}
					oldLabel={t('old_label')}
				/>
			</div>
		{/if}
	</div>
{/if}

<!-- ── Literature ── -->
<Expander title={t('literature')}>
	<p>{@html marked(t('literature_onpage'))}</p>
	<ul>
		<li>
			Matuszyńska, A., Heidari, S., Jahns, P., &amp; Ebenhöh, O. (2016). A mathematical model of
			non-photochemical quenching to study short-term light memory in plants.
			<em>Biochimica et Biophysica Acta (BBA) - Bioenergetics</em>, 1857(12), 1860–1869.
			<a href="https://doi.org/10.1016/j.bbabio.2016.09.003" target="_blank" rel="noopener"
				>https://doi.org/10.1016/j.bbabio.2016.09.003</a
			>
		</li>
	</ul>
</Expander>

<PageNav
	prev={{ href: '/experiments', label: 'Experiments in Silico' }}
	next={{ href: '/conclusion', label: 'Conclusion' }}
/>

<style>
	.prose :global(h1),
	.prose :global(h2),
	.prose :global(h3),
	.prose :global(h4) {
		margin-top: var(--space-5);
		margin-bottom: var(--space-2);
		line-height: 1.3;
	}

	.intro-content {
		margin: var(--space-4) 0;
	}

	.intro-content :global(a) {
		color: var(--color-primary);
	}

	.fig {
		margin: var(--space-6) auto;
		text-align: center;
		max-width: 60%;
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

	.protocol-img {
		max-width: 100%;
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

	.slider-row.three {
		grid-template-columns: repeat(3, 1fr);
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

		.slider-row,
		.slider-row.three {
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
