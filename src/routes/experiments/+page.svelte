<script lang="ts">
	import { base } from '$app/paths';
	import { Accordion as Expander } from '@computational-biology-aachen/design';
	import { InfoBox } from '@computational-biology-aachen/design';
	import { PageNav } from '@computational-biology-aachen/design';
	import ActivationSliders from '$lib/components/simulation/ActivationSliders.svelte';
	import CompareCheckbox from '$lib/components/simulation/CompareCheckbox.svelte';
	import LiteratureExpander from '$lib/components/simulation/LiteratureExpander.svelte';
	import { Button } from '@computational-biology-aachen/design';
	import type { PhaseRegion } from '$lib/components/simulation/SimChart.svelte';
	import SimResultsGrid from '$lib/components/simulation/SimResultsGrid.svelte';
	import { ta } from '$lib/i18n';
	import * as m from '$lib/paraglide/messages';
	import { buildPamProtocol } from '$lib/simulations/pam';
	import { audienceStore } from '$lib/stores/audience.svelte';
	import { LOG_STEPS, SimState } from '$lib/stores/simState.svelte';
	import { marked } from 'marked';
	import Katex from 'svelte-katex';

	const sim = new SimState();
	sim.setup();

	// Slider state
	let lightIntensity = $state(100);
	let totalMinutes = $state(5);
	let pulseInterval = $state(85);
	let darkLength = $state(30);
	let saturatingPulse = $state(5000);
	let compareWithLast = $state(true);
	let showAnswers = $state(false);

	// Logspace sliders
	let activationIdx = $state(10); // LOG_STEPS[10] = 100
	let deactivationIdx = $state(10);
	const activationMultiplier = $derived(LOG_STEPS[activationIdx]);
	const deactivationMultiplier = $derived(LOG_STEPS[deactivationIdx]);
	const totalTime = $derived(totalMinutes * 60);

	function runSimulation() {
		const protocol = buildPamProtocol({
			lightIntensity,
			saturatingPulse,
			totalMinutes,
			darkLength,
			pulseInterval
		});
		const kDeepoxV = 0.0024 * (activationMultiplier / 100);
		const kEpoxZ = 0.00024 * (deactivationMultiplier / 100);
		sim.run(protocol, { AL: lightIntensity, SP: saturatingPulse, CtZ: kDeepoxV, CtV: kEpoxZ }, [
			kDeepoxV,
			kEpoxZ
		]);
	}

	const phases = $derived.by<PhaseRegion[]>(() => [
		{ start: 0, end: darkLength, color: 'rgba(28, 91, 199, 0.18)' },
		{ start: darkLength, end: totalTime, color: 'rgba(207, 109, 12, 0.18)' }
	]);

	const showOld = $derived(compareWithLast && sim.previousResult !== null);

	const paramRows = $derived.by(() => {
		const cp = sim.currentParams;
		const pp = sim.previousParams;
		if (!cp) return [];
		return [
			{ label: 'AL [μmol m⁻² s⁻¹]', newVal: cp.AL, oldVal: pp?.AL },
			{ label: 'SP [μmol m⁻² s⁻¹]', newVal: cp.SP, oldVal: pp?.SP },
			{ label: 'CtZ [s⁻¹]', newVal: cp.CtZ.toFixed(5), oldVal: pp?.CtZ?.toFixed(5) },
			{ label: 'CtV [s⁻¹]', newVal: cp.CtV.toFixed(6), oldVal: pp?.CtV?.toFixed(6) }
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

<PageNav {base}
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
				<ActivationSliders
					bind:activationIdx
					bind:deactivationIdx
					{activationMultiplier}
					{deactivationMultiplier}
				/>
			</div>
			<div class="slider-col">
				<label class="slider-label">
					{@html m.fal_slider_darklength()}: <strong>{darkLength} s</strong>
					<input type="range" min="0" max={totalMinutes * 60} step="5" bind:value={darkLength} />
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
		<Button loading={sim.loading} fullWidth onclick={runSimulation}>{sim.loading ? 'Running…' : 'Run simulation'}</Button>
	</div>
	<CompareCheckbox bind:checked={compareWithLast} />
</div>

{#if sim.errorMsg}
	<p class="error-msg">{sim.errorMsg}</p>
{/if}

<!-- Results ---------------------------------------- -->
{#if sim.currentResult}
	<SimResultsGrid
		currentResult={sim.currentResult}
		previousResult={sim.previousResult}
		{showOld}
		{phases}
		{totalTime}
		{paramRows}
		showOldParams={showOld && sim.previousParams !== null}
	/>
{/if}

<LiteratureExpander />

<PageNav {base}
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

	.slider-col {
		display: flex;
		flex-direction: column;
		gap: var(--space-3);
	}
</style>
