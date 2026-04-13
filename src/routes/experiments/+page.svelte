<script lang="ts">
	import { base } from '$app/paths';
	import Expander from '$lib/components/Expander.svelte';
	import InfoBox from '$lib/components/InfoBox.svelte';
	import PageNav from '$lib/components/PageNav.svelte';
	import CompareCheckbox from '$lib/components/simulation/CompareCheckbox.svelte';
	import ParameterTable from '$lib/components/simulation/ParameterTable.svelte';
	import RunButton from '$lib/components/simulation/RunButton.svelte';
	import type { PhaseRegion } from '$lib/components/simulation/SimChart.svelte';
	import SimChart from '$lib/components/simulation/SimChart.svelte';
	import { ta } from '$lib/i18n';
	import * as m from '$lib/paraglide/messages';
	import { buildPamProtocol } from '$lib/simulations/pam';
	import { audienceStore } from '$lib/stores/audience.svelte';
	import { WorkerManager, simWorker, type Res } from '$lib/stores/workerStore';
	import { marked } from 'marked';
	import { onDestroy, onMount } from 'svelte';
	import Katex from 'svelte-katex';

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
	let totalMinutes = $state(5);
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

	// Model code constants (4math walkthrough)
	const CODE = {
		define: `import numpy as np\nfrom modelbase.ode import Model\n\nmodel = Model()`,
		params: `pars = {\n    "PSIItot": 2.5, "PQtot": 20, "APtot": 50, ...\n    "kDeepoxV": 0.0024,   # Activation of quenching\n    "kEpoxZ":   0.00024,  # Deactivation\n    # ... (see full parameter list on GitHub)\n}`,
		comps: `comps = ["P", "H", "E", "A", "Pr", "V"]`,
		addCompsPars: `model.add_parameters(pars)\nmodel.add_compounds(comps)`,
		definesim: `from modelbase.ode import Simulator\nsimulator = Simulator(model)`,
		initialisesim: `y0 = {"P": 0, "H": 6.32975752e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}\nsimulator.initialise(y0)`
	};
</script>

<svelte:head>
	<title>Experiments in Silico</title>
</svelte:head>

<h1>{@html marked(m.fal_headline_experiments())}</h1>

<InfoBox>
	{@html marked(ta(m.bio_fal_learning_objectives(), m.math_fal_learning_objectives()))}
</InfoBox>

<PageNav
	prev={{ href: '/model', label: 'Computational Models' }}
	next={{ href: '/plant-memory', label: 'Plant Memory' }}
/>

<!-- Model Construction ----------------------------- -->
<div class="prose">{@html marked(m.fal_headline_model_construction())}</div>

<p>{@html marked(m.fal_construction_explanation_1())}</p>

<figure class="fig">
	<img src="{base}/pictures/NPQphotosynthesis.png" alt={m.fal_caption_model_npq()} />
	<figcaption>{m.fal_caption_model_npq()}</figcaption>
</figure>

<p>{@html marked(m.fal_construction_explanation_2())}</p>
<p>{@html m.fal_rates_1()}</p>
<p>{@html marked(m.fal_rates_2())}</p>
<p>{@html marked(m.fal_rates_3())}</p>
<p>{@html marked(m.fal_rates_4())}</p>
<p>{@html marked(m.fal_rates_5())}</p>
<p>{@html m.fal_rates_6()}</p>

<Expander title={m.fal_components_explanation_header()}>
	<div>{@html marked(m.fal_molecules_explanation_table())}</div>
	<div>{@html marked(m.fal_enzymes_explanation_table())}</div>
</Expander>

<!-- 4math: ODE equations + code walkthrough -->
{#if audienceStore.audience === '4math'}
	<div class="prose">{@html marked(m.math_fal_headline_model_equations())}</div>
	<p>{@html marked(m.math_fal_model_equations_introduction())}</p>

	<div class="math-block">
		<Katex displayMode
			>{String.raw`\begin{aligned}
\frac{\mathrm{dPQH_2}}{\mathrm{d}t} &= v_\mathrm{PSII} - v_\mathrm{PQ_{ox}} \\
\frac{\mathrm{dATP}}{\mathrm{d}t} &= v_\mathrm{ATPsynthase} - v_\mathrm{ATPconsumption} \\
\frac{\mathrm{dATPase^{*}}}{\mathrm{d}t} &= F k_\mathrm{actATPase} \cdot \mathrm{H(PFD)} \cdot \mathrm{ATPase} - k_\mathrm{deactATPase} \cdot (1 - \mathrm{H(PFD)}) \cdot \mathrm{ATPase^{*}} \\
b_\mathrm{H} \cdot \frac{\mathrm{dH}}{\mathrm{d}t} &= 2 v_\mathrm{PSII} + 4 v_\mathrm{PQ_{ox}} - \tfrac{14}{3} v_\mathrm{ATPsynthase} - v_\mathrm{leak} \\
\frac{\mathrm{dPsbS}}{\mathrm{d}t} &= -v_\mathrm{Psbs^{p}} \\
\frac{\mathrm{dVx}}{\mathrm{d}t} &= -v_\mathrm{Xcyc}
\end{aligned}`}</Katex
		>
	</div>

	<Expander title={m.math_fal_reaction_rates()}>
		<p>{@html marked(m.math_fal_rates_dynamic())}</p>
		<div class="math-block">
			<Katex displayMode
				>{String.raw`\begin{aligned}
v_{\mathrm{PSII}} &= k_2 \cdot 0.5 \cdot B_1 \\
v_\mathrm{Xcyc} &= k_\mathrm{DeepoxV} \cdot \frac{H^{nH_X}}{H^{nH_X} + pH_{\mathrm{inv}}(K_\mathrm{phSat})^{nH_X}} \cdot \mathrm{Vx} - k_\mathrm{EpoxZ} \cdot (\mathrm{X^{tot}} - \mathrm{Vx}) \\
Q &= \gamma_0 (1-\tfrac{Z}{Z+K_{ZSat}}) \mathrm{PsbS} + \gamma_1 (1-\tfrac{Z}{Z+K_{ZSat}}) \mathrm{PsbS^p} + \gamma_2 \tfrac{Z}{Z+K_{ZSat}} \mathrm{PsbS^p} + \gamma_3 \tfrac{Z}{Z+K_{ZSat}} \mathrm{PsbS}
\end{aligned}`}</Katex
			>
		</div>
	</Expander>

	<Expander title={m.math_fal_model_code_expander()}>
		<div class="prose">{@html marked(m.math_fal_construction_header())}</div>
		<p>{@html marked(m.math_fal_construction_1())}</p>
		<pre><code>{CODE.define}</code></pre>

		<p>{@html marked(m.math_fal_construction_2())}</p>
		<details>
			<summary>Parameters</summary>
			<pre><code>{CODE.params}</code></pre>
		</details>
		<details>
			<summary>Compounds</summary>
			<pre><code>{CODE.comps}</code></pre>
		</details>

		<p>{@html marked(m.math_fal_construction_3())}</p>
		<pre><code>{CODE.addCompsPars}</code></pre>

		<div class="prose">{@html marked(m.math_fal_simulation_header())}</div>
		<p>{@html marked(m.math_fal_simulation_1())}</p>
		<pre><code>{CODE.definesim}</code></pre>

		<p>{@html marked(m.math_fal_simulation_2())}</p>
		<pre><code>{CODE.initialisesim}</code></pre>
	</Expander>
{/if}

<!-- Implementation -->
<div class="prose">{@html marked(m.fal_headline_implementation())}</div>
<p>
	{@html marked(
		ta(m.bio_fal_implementation_description(), m.math_fal_implementation_description())
	)}
</p>
{#if audienceStore.audience === '4bio'}
	<p>{@html m.bio_fal_implementation_to_expert()}</p>
{/if}

<!-- Analysis --------------------------------------- -->
<div class="prose">{@html marked(m.fal_headline_analyse())}</div>
<p>{@html marked(ta(m.bio_fal_introduktion(), m.math_fal_introduktion()))}</p>

<div class="prose">{@html marked(m.fal_headline_slider())}</div>
<p>{@html marked(m.fal_explanatnion())}</p>

<Expander title={m.fal_graph_explanation_expander()} open>
	<div class="prose">{@html marked(m.fal_graph_explanation_header_single())}</div>
	<p>{@html marked(m.fal_graph_explanation_1())}</p>
	<div class="math-inline">
		<Katex displayMode>{"NPQ = \\dfrac{F_m - F_m'}{F_m'}"}</Katex>
	</div>
	<p>{@html ta(m.bio_fal_graph_explanation_2(), m.math_fal_graph_explanation_2())}</p>
	<div class="prose">{@html marked(m.fal_graph_explanation_header_duo())}</div>
	<p>{@html marked(m.fal_graph_explanation_duo())}</p>
</Expander>

<Expander title={m.fal_guiding_expander()} open>
	<div class="prose">{@html marked(m.fal_guiding_header())}</div>
	<label class="toggle-label">
		<input type="checkbox" bind:checked={showAnswers} />
		{@html marked.parseInline(m.fal_guiding_toggle())}
	</label>
	{#if !showAnswers}
		<div class="qa-text">{@html marked(m.fal_guiding_questions())}</div>
		{#if audienceStore.audience === '4bio'}
			<div class="qa-text">{@html marked(m.bio_fal_guiding_questions_extend())}</div>
		{/if}
	{:else}
		<div class="qa-text">{@html marked(m.fal_guiding_answers())}</div>
		{#if audienceStore.audience === '4bio'}
			<div class="qa-text">{@html marked(m.bio_fal_guiding_answers_extend())}</div>
		{/if}
	{/if}
</Expander>

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
		<div class="charts-grid" class:three-cols={audienceStore.audience === '4bio'}>
			<div class="chart-card">
				<p class="chart-label">{ta(m.bio_fluo(), m.math_fluo())}</p>
				<SimChart
					xNew={currentResult.time}
					yNew={currentResult.fluo}
					xOld={showOld && previousResult ? previousResult.time : []}
					yOld={showOld && previousResult ? previousResult.fluo : []}
					{phases}
					yLabel={ta(m.bio_fluo(), m.math_fluo())}
					showLine={true}
					{totalTime}
				/>
			</div>

			{#if audienceStore.audience === '4bio'}
				<div class="chart-card">
					<p class="chart-label">{m.axis_npq()}</p>
					<SimChart
						xNew={currentResult.npqTime}
						yNew={currentResult.npq}
						xOld={showOld && previousResult ? previousResult.npqTime : []}
						yOld={showOld && previousResult ? previousResult.npq : []}
						{phases}
						yLabel={m.axis_npq()}
						showLine={false}
						{totalTime}
					/>
				</div>

				<div class="chart-card">
					<p class="chart-label">{m.axis_phipsii()}</p>
					<SimChart
						xNew={currentResult.npqTime}
						yNew={currentResult.phiPsii}
						xOld={showOld && previousResult ? previousResult.npqTime : []}
						yOld={showOld && previousResult ? previousResult.phiPsii : []}
						{phases}
						yLabel={m.axis_phipsii()}
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
					newLabel={m.new_label()}
					oldLabel={m.old_label()}
				/>
			</div>
		{/if}
	</div>
{/if}

<!-- Literature -->
<Expander title={m.literature()}>
	<p>{@html marked(m.literature_onpage())}</p>
	<ul>
		<li>
			Matuszyńska, A., Heidari, S., Jahns, P., &amp; Ebenhöh, O. (2016). A mathematical model of
			non-photochemical quenching to study short-term light memory in plants.
			<em>Biochimica et Biophysica Acta (BBA) - Bioenergetics</em>, 1857(12), 1860-1869.
			<a href="https://doi.org/10.1016/j.bbabio.2016.09.003" target="_blank" rel="noopener"
				>https://doi.org/10.1016/j.bbabio.2016.09.003</a
			>
		</li>
	</ul>
</Expander>

<PageNav
	prev={{ href: '/model', label: 'Computational Models' }}
	next={{ href: '/plant-memory', label: 'Plant Memory' }}
/>

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
