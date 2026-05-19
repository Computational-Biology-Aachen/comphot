<script lang="ts">
  import { base } from "$app/paths";

  import { ta } from "$lib/i18n";
  import * as m from "$lib/paraglide/messages";
  import SimResultsGrid from "$lib/SimResultsGrid.svelte";
  import { buildPamProtocol } from "$lib/simulations/pam";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import { LOG_STEPS, SimState } from "$lib/stores/simState.svelte";
  import {
    ActivationSliders,
    Button,
    CompareCheckbox,
    Accordion as Expander,
    H1,
    H2,
    InfoBox,
    LiteratureExpander,
    Main,
    Narrow,
    PageNav,
    type PhaseRegion,
    Text,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";
  import Katex from "svelte-katex";

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
      pulseInterval,
    });
    const kDeepoxV = 0.0024 * (activationMultiplier / 100);
    const kEpoxZ = 0.00024 * (deactivationMultiplier / 100);
    sim.run(
      protocol,
      { AL: lightIntensity, SP: saturatingPulse, CtZ: kDeepoxV, CtV: kEpoxZ },
      [kDeepoxV, kEpoxZ],
    );
  }

  const phases = $derived.by<PhaseRegion[]>(() => [
    { start: 0, end: darkLength, color: "rgba(28, 91, 199, 0.18)" },
    { start: darkLength, end: totalTime, color: "rgba(207, 109, 12, 0.18)" },
  ]);

  const showOld = $derived(compareWithLast && sim.previousResult !== null);

  const paramRows = $derived.by(() => {
    const cp = sim.currentParams;
    const pp = sim.previousParams;
    if (!cp) return [];
    return [
      { label: "AL [μmol m⁻² s⁻¹]", newVal: cp.AL, oldVal: pp?.AL },
      { label: "SP [μmol m⁻² s⁻¹]", newVal: cp.SP, oldVal: pp?.SP },
      {
        label: "CtZ [s⁻¹]",
        newVal: cp.CtZ.toFixed(5),
        oldVal: pp?.CtZ?.toFixed(5),
      },
      {
        label: "CtV [s⁻¹]",
        newVal: cp.CtV.toFixed(6),
        oldVal: pp?.CtV?.toFixed(6),
      },
    ];
  });

  // Model code constants (4math walkthrough)
  const CODE = {
    define: `import numpy as np\nfrom modelbase.ode import Model\n\nmodel = Model()`,
    params: `pars = {\n    "PSIItot": 2.5, "PQtot": 20, "APtot": 50, ...\n    "kDeepoxV": 0.0024,   # Activation of quenching\n    "kEpoxZ":   0.00024,  # Deactivation\n    # ... (see full parameter list on GitHub)\n}`,
    comps: `comps = ["P", "H", "E", "A", "Pr", "V"]`,
    addCompsPars: `model.add_parameters(pars)\nmodel.add_compounds(comps)`,
    definesim: `from modelbase.ode import Simulator\nsimulator = Simulator(model)`,
    initialisesim: `y0 = {"P": 0, "H": 6.32975752e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}\nsimulator.initialise(y0)`,
  };
</script>

<svelte:head>
  <title>Experiments in Silico</title>
</svelte:head>

<Main>
  <Narrow>
    <H1>{@html marked.parseInline(m.fal_headline_experiments())}</H1>

    <InfoBox>
      <!-- FIXME: break message into smaller pieces -->
      {@html marked.parse(
        ta(m.bio_fal_learning_objectives(), m.math_fal_learning_objectives()),
      )}
    </InfoBox>

    <PageNav
      base={base}
      prev={{ href: "/model", label: "Computational Models" }}
      next={{ href: "/plant-memory", label: "Plant Memory" }}
    />

    <!-- Model Construction ----------------------------- -->
    <H2>
      {@html marked.parseInline(m.fal_headline_model_construction())}
    </H2>

    <Text>
      {@html marked.parseInline(m.fal_construction_explanation_1())}
    </Text>

    <figure class="fig">
      <img
        src="{base}/pictures/NPQphotosynthesis.png"
        alt={m.fal_caption_model_npq()}
      />
      <figcaption>{m.fal_caption_model_npq()}</figcaption>
    </figure>

    <Text>{@html marked.parseInline(m.fal_construction_explanation_2())}</Text>
    <Text>{@html marked.parseInline(m.fal_rates_1())}</Text>
    <Text>{@html marked.parseInline(m.fal_rates_2())}</Text>
    <Text>{@html marked.parseInline(m.fal_rates_3())}</Text>
    <Text>{@html marked.parseInline(m.fal_rates_4())}</Text>
    <Text>{@html marked.parseInline(m.fal_rates_5())}</Text>
    <Text>{@html marked.parseInline(m.fal_rates_6())}</Text>

    <Expander title={m.fal_components_explanation_header()}>
      <Text
        >{@html marked.parseInline(m.fal_molecules_explanation_table())}</Text
      >
      <Text>{@html marked.parseInline(m.fal_enzymes_explanation_table())}</Text>
    </Expander>

    <!-- 4math: ODE equations + code walkthrough -->
    {#if audienceStore.audience === "4math"}
      <H2>
        {@html marked.parseInline(m.math_fal_headline_model_equations())}
      </H2>
      <Text>
        {@html marked.parseInline(m.math_fal_model_equations_introduction())}
      </Text>

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
        <Text>{@html marked.parseInline(m.math_fal_rates_dynamic())}</Text>
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
        <Text>
          {@html marked.parseInline(m.math_fal_construction_header())}
        </Text>
        <Text>{@html marked.parseInline(m.math_fal_construction_1())}</Text>
        <pre><code>{CODE.define}</code></pre>

        <Text>{@html marked.parseInline(m.math_fal_construction_2())}</Text>
        <details>
          <summary>Parameters</summary>
          <pre><code>{CODE.params}</code></pre>
        </details>
        <details>
          <summary>Compounds</summary>
          <pre><code>{CODE.comps}</code></pre>
        </details>

        <Text>{@html marked.parseInline(m.math_fal_construction_3())}</Text>
        <pre><code>{CODE.addCompsPars}</code></pre>

        <Text>{@html marked.parseInline(m.math_fal_simulation_header())}</Text>
        <Text>{@html marked.parseInline(m.math_fal_simulation_1())}</Text>
        <pre><code>{CODE.definesim}</code></pre>

        <Text>{@html marked.parseInline(m.math_fal_simulation_2())}</Text>
        <pre><code>{CODE.initialisesim}</code></pre>
      </Expander>
    {/if}

    <!-- Implementation -->
    <H2>{@html marked.parseInline(m.fal_headline_implementation())}</H2>
    <Text>
      {@html marked.parseInline(
        ta(
          m.bio_fal_implementation_description(),
          m.math_fal_implementation_description(),
        ),
      )}
    </Text>
    {#if audienceStore.audience === "4bio"}
      <Text>{@html m.bio_fal_implementation_to_expert()}</Text>
    {/if}

    <!-- Analysis --------------------------------------- -->
    <H2>{@html marked.parseInline(m.fal_headline_analyse())}</H2>
    <Text>
      {@html marked.parseInline(
        ta(m.bio_fal_introduktion(), m.math_fal_introduktion()),
      )}
    </Text>

    <Text>{@html marked.parseInline(m.fal_headline_slider())}</Text>
    <Text>{@html marked.parseInline(m.fal_explanatnion())}</Text>

    <Expander
      title={m.fal_graph_explanation_expander()}
      open={false}
    >
      <Text>
        {@html marked.parseInline(m.fal_graph_explanation_header_single())}
      </Text>
      <Text>{@html marked.parseInline(m.fal_graph_explanation_1())}</Text>
      <div class="math-inline">
        <Katex displayMode>{"NPQ = \\dfrac{F_m - F_m'}{F_m'}"}</Katex>
      </div>
      <Text>
        {@html ta(
          m.bio_fal_graph_explanation_2(),
          m.math_fal_graph_explanation_2(),
        )}
      </Text>
      <Text>
        {@html marked.parseInline(m.fal_graph_explanation_header_duo())}
      </Text>
      <Text>{@html marked.parseInline(m.fal_graph_explanation_duo())}</Text>
    </Expander>

    <!-- Having trouble connecting -->
    <Expander
      title={m.fal_guiding_expander()}
      open={false}
    >
      <Text>{@html marked.parseInline(m.fal_guiding_header())}</Text>
      <label class="toggle-label">
        <input
          type="checkbox"
          bind:checked={showAnswers}
        />
        {@html marked.parseInline(m.fal_guiding_toggle())}
      </label>
      {#if !showAnswers}
        <!-- FIXME: break message into smaller pieces -->
        {@html marked.parse(m.fal_guiding_questions())}

        {#if audienceStore.audience === "4bio"}
          {@html marked.parseInline(m.bio_fal_guiding_questions_extend())}
        {/if}
      {:else}
        {@html marked.parseInline(m.fal_guiding_answers())}
        {#if audienceStore.audience === "4bio"}
          {@html marked.parseInline(m.bio_fal_guiding_answers_extend())}
        {/if}
      {/if}
    </Expander>

    <!-- Slider controls -------------------------------- -->
    <div class="slider-section">
      <label class="slider-label">
        {@html m.slider_light()}: <strong>{lightIntensity}</strong>
        <input
          type="range"
          min="50"
          max="900"
          step="50"
          bind:value={lightIntensity}
        />
      </label>

      <div class="slider-row">
        <label class="slider-label">
          {@html m.fal_slider_time()}: <strong>{totalMinutes} min</strong>
          <input
            type="range"
            min="1"
            max="15"
            step="1"
            bind:value={totalMinutes}
          />
        </label>
        <label class="slider-label">
          {@html m.slider_pulses()}: <strong>{pulseInterval} s</strong>
          <input
            type="range"
            min="5"
            max="150"
            step="5"
            bind:value={pulseInterval}
          />
        </label>
      </div>

      {#if audienceStore.audience === "4bio"}
        <div class="slider-row">
          <div class="slider-col">
            <ActivationSliders
              bind:activationIdx={activationIdx}
              bind:deactivationIdx={deactivationIdx}
              activationMultiplier={activationMultiplier}
              deactivationMultiplier={deactivationMultiplier}
              activationLabel={m.slider_activation()}
              deactivationLabel={m.slider_deactivation()}
            />
          </div>
          <div class="slider-col">
            <label class="slider-label">
              {@html m.fal_slider_darklength()}: <strong>{darkLength} s</strong>
              <input
                type="range"
                min="0"
                max={totalMinutes * 60}
                step="5"
                bind:value={darkLength}
              />
            </label>
            <label class="slider-label">
              {@html m.fal_slider_saturate()}:
              <strong>{saturatingPulse}</strong>
              <input
                type="range"
                min="0"
                max="10000"
                step="500"
                bind:value={saturatingPulse}
              />
            </label>
          </div>
        </div>
      {/if}
    </div>

    <!-- Run controls -->
    <div class="run-controls">
      <div class="run-btn-wrap">
        <Button
          loading={sim.loading}
          fullWidth
          onclick={runSimulation}
          >{sim.loading ? "Running…" : "Run simulation"}</Button
        >
      </div>
      <CompareCheckbox bind:checked={compareWithLast} />
    </div>

    {#if sim.errorMsg}
      <Text>{sim.errorMsg}</Text>
    {/if}

    <!-- Results ---------------------------------------- -->
    {#if sim.currentResult}
      <SimResultsGrid
        currentResult={sim.currentResult}
        previousResult={sim.previousResult}
        showOld={showOld}
        phases={phases}
        totalTime={totalTime}
        paramRows={paramRows}
        showOldParams={showOld && sim.previousParams !== null}
      />
    {/if}

    <LiteratureExpander />

    <PageNav
      base={base}
      prev={{ href: "/model", label: "Computational Models" }}
      next={{ href: "/plant-memory", label: "Plant Memory" }}
    />
  </Narrow>
</Main>
