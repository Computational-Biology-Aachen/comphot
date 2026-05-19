<script lang="ts">
  import { base } from "$app/paths";
  import { ta } from "$lib/i18n";
  import * as m from "$lib/paraglide/messages";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import VideoTranscriptToggle, {
    Accordion as Expander,
    InfoBox,
    PageNav,
    YouTubeEmbed,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";
  import Katex from "svelte-katex";

  // Python code snippets for 4math tabs
  const sirV1Integ = `from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from cycler import cycler


def sir(t, y, alpha, beta):
    s, i, r = y
    infection = alpha * s * i / (s + i + r)
    recovery = beta * i
    return (
        -infection,  # ds/dt
        infection - recovery,  # di/dt
        recovery,  # dr/dt
    )


res = solve_ivp(
    sir,
    t_span=(0, 20),
    y0=(900, 100, 0),  # needs to match s, i, r unpacking order
    args=(2, 0.5),  # needs to match fn argument order
)`;

  const sirV1Plot = `# To get the same design as us
text_color = "#727682"

with plt.rc_context({
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.edgecolor": text_color,
    "font.size": 12.0,
    "text.color": text_color,
    "axes.prop_cycle": cycler(color=["#f9a51b", "#d1232a", "#1062ef"])
}):
    fig, ax = plt.subplots(figsize=(7, 4))
    for i in ['S', 'I', 'R']:
        ax.plot(res['t'], res['y'][['S', 'I', 'R'].index(i)],
                label=i, linestyle='solid', linewidth=5)

plt.xlabel('Time [Months]', fontsize=12, weight='bold')
plt.ylabel('Population size [a.u.]', fontsize=12, weight='bold')
plt.xlim(0); plt.ylim(0)
plt.legend(loc='center right', frameon=False)
plt.tight_layout()
plt.show()`;

  const sirV2RateFns = `from modelbase.ode import Model, Simulator

def infection(beta, s, i, r):
    return beta * s * i / (s + i + r)

def recovery(gamma, x):
    return gamma * x`;

  const sirV2Model = `sir = Model()
sir.add_compounds(["S", "I", "R"])
sir.add_parameters({"beta": 2, "gamma": 0.5})`;

  const sirV2Reactions = `sir.add_reaction_from_args("infection", infection, {"S": -1, "I": 1}, ["beta", "S", "I", "R"])
sir.add_reaction_from_args("recovery", recovery, {"I": -1, "R": 1}, ["gamma", "I"])`;

  const sirV2Simulation = `s = Simulator(sir)
s.initialise({"S": 900, "I": 100, "R": 0})
res = s.simulate(t_end=20)
s.plot(xlabel="Time [Months]", ylabel="Population size [a.u.]")`;

  const sird = `sird = sir.copy()
sird.add_compound("d")
sird.add_parameter("mu", 0.05)
sird.add_reaction_from_args("death", proportional, {"i": -1, "d": 1}, ["mu", "i"])`;

  let activeTab = $state<"sir" | "manual" | "modelbase">("sir");
</script>

<svelte:head>
  <title>{m.mdl_headline_computational_models()} | ComPhot</title>
</svelte:head>

<article class="page-content">
  <div class="prose">
    {@html marked(m.mdl_headline_computational_models())}
  </div>

  <InfoBox>
    <div class="prose">
      {@html marked(
        ta(m.bio_mdl_learning_objectives(), m.math_mdl_learning_objectives()),
      )}
    </div>
  </InfoBox>

  <PageNav
    base={base}
    prev={{ href: "/method", label: m.sde_pagenames_measuringmethod() }}
    next={{
      href: "/experiments",
      label: m.sde_pagenames_experimentsinsilico(),
    }}
  />

  <section>
    <div class="prose">
      {@html marked(m.mdl_headline_model())}
      {@html marked(m.mdl_mathematical_modelling_explanation_1())}
    </div>

    <figure class="page-figure">
      <img
        src="{base}/pictures/Modeling_scheme_eng.png"
        alt="Modeling cycle diagram"
        class="page-img centered"
      />
      <figcaption class="caption">
        {m.mdl_caption_modelling_picture()}
      </figcaption>
    </figure>

    <div class="prose">
      {@html marked(m.mdl_mathematical_modelling_explanation_1b())}
    </div>

    <YouTubeEmbed
      videoId="oVME5KIHrO8"
      title="Building mathematical models"
    />
    <VideoTranscriptToggle
      message={m.expander_video_transcript()}
      transcript={m.mdl_video_transcript_models()}
    />
  </section>

  <section>
    <div class="prose">
      {@html marked(m.mdl_example_mathematical_model())}
    </div>

    <!-- Tabbed SIR section -->
    <div class="tabs">
      <div
        class="tab-list"
        role="tablist"
      >
        <button
          role="tab"
          aria-selected={activeTab === "sir"}
          class:active={activeTab === "sir"}
          onclick={() => (activeTab = "sir")}
        >
          {m.mdl_tab_sir()}
        </button>
        {#if audienceStore.audience === "4math"}
          <button
            role="tab"
            aria-selected={activeTab === "manual"}
            class:active={activeTab === "manual"}
            onclick={() => (activeTab = "manual")}
          >
            {m.math_mdl_tab_manual()}
          </button>
          <button
            role="tab"
            aria-selected={activeTab === "modelbase"}
            class:active={activeTab === "modelbase"}
            onclick={() => (activeTab = "modelbase")}
          >
            {m.math_mdl_tab_modelbase()}
          </button>
        {/if}
      </div>

      <div class="tab-panel">
        {#if activeTab === "sir"}
          <div class="prose">
            {@html marked(m.mdl_headline_sir())}
            {@html marked(
              ta(
                m.bio_mdl_mathematical_modelling_example(),
                m.math_mdl_mathematical_modelling_example(),
              ),
            )}
          </div>

          {#if audienceStore.audience === "4bio"}
            <figure class="page-figure">
              <img
                src="{base}/pictures/SIR_Aliens.png"
                alt="SIR Aliens diagram"
                class="page-img half-width"
              />
            </figure>
          {:else}
            <div class="katex-block">
              <Katex displayMode
                >{"\\mathrm{S} \\xrightarrow{\\textit{v}_1} \\mathrm{I} \\xrightarrow{\\textit{v}_2} \\mathrm{R}"}</Katex
              >
              <Katex displayMode
                >{"\\begin{aligned} v_1 &= \\beta \\cdot \\frac{\\mathrm{S}\\cdot \\mathrm{I}}{\\mathrm{N}} \\\\ v_2 &= \\gamma \\cdot \\mathrm{I} \\\\ \\end{aligned}"}</Katex
              >
            </div>
          {/if}

          <div class="prose">
            {@html marked(
              ta(
                m.bio_mdl_mathematical_modelling_example_1(),
                m.math_mdl_mathematical_modelling_example_1(),
              ),
            )}
          </div>

          {#if audienceStore.audience === "4bio"}
            <figure class="page-figure">
              <img
                src="{base}/pictures/SIR_AliensScheme.png"
                alt="SIR Aliens scheme"
                class="page-img half-width"
              />
            </figure>
          {:else}
            <div class="katex-block">
              <Katex displayMode
                >{"\\mathrm{S} \\xrightarrow{\\textit{v}_1} \\mathrm{I} \\xrightarrow{\\textit{v}_2} \\mathrm{R}"}</Katex
              >
              <Katex displayMode
                >{"\\begin{aligned} \\frac{\\mathrm{d}\\mathrm{S}}{\\mathrm{d}t} &= - v_1 \\\\ \\frac{\\mathrm{d}\\mathrm{I}}{\\mathrm{d}t} &= v_1 - v_2 \\\\ \\frac{\\mathrm{d}\\mathrm{R}}{\\mathrm{d}t} &= v_2 \\end{aligned}"}</Katex
              >
            </div>
          {/if}

          <div class="prose">
            {@html marked(
              ta(
                m.bio_mdl_mathematical_modelling_example_2(),
                m.math_mdl_mathematical_modelling_example_2(),
              ),
            )}
          </div>

          {#if audienceStore.audience === "4bio"}
            <div class="katex-block">
              <Katex displayMode
                >{"\\begin{aligned} \\mathrm{Infecting\\ rate:\\ } v_1 &= \\beta \\cdot \\frac{\\mathrm{S}\\cdot \\mathrm{I}}{\\mathrm{N}} \\\\ \\mathrm{Recovery\\ rate:\\ } v_{2} &= \\gamma \\cdot \\mathrm{I} \\\\ \\end{aligned}"}</Katex
              >
            </div>
            <div class="prose">
              {@html marked(m.bio_mdl_mathematical_modelling_example_3())}
            </div>
            <div class="katex-block">
              <Katex displayMode
                >{"\\begin{aligned} \\mathrm{dS} &= -v_1 \\cdot \\mathrm{d}t \\\\ \\mathrm{dI} &= \\left( v_1 - v_2 \\right) \\cdot \\mathrm{d}t \\\\ \\mathrm{dR} &= v_2 \\cdot \\mathrm{d}t \\end{aligned}"}</Katex
              >
            </div>
            <div class="prose">
              {@html marked(m.bio_mdl_mathematical_modelling_example_4())}
            </div>
          {/if}

          <div class="prose">
            {@html marked(
              ta(
                m.bio_mdl_mathematical_modelling_example_simple(),
                m.math_mdl_mathematical_modelling_example_simple(),
              ),
            )}
          </div>
        {:else if activeTab === "manual"}
          <div class="prose">
            {@html marked(m.math_mdl_headline_manual())}
          </div>
          <pre class="code-block"><code>{sirV1Integ}</code></pre>
          <div class="prose">
            {@html marked(m.math_mdl_sir_implementation_manual_1())}
          </div>
          <figure class="page-figure">
            <img
              src="{base}/pictures/SIR_manual.png"
              alt="SIR model manual plot"
              class="page-img half-width"
            />
          </figure>
          <pre class="code-block"><code>{sirV1Plot}</code></pre>
          <div class="prose">
            {@html marked(m.math_mdl_sir_implementation_manual_2())}
          </div>
        {:else if activeTab === "modelbase"}
          <div class="prose">
            {@html marked(m.math_mdl_headline_modelbase())}
            {@html marked(m.math_mdl_sir_implementation_modelbase_1())}
          </div>
          <pre class="code-block"><code>{sirV2RateFns}</code></pre>
          <div class="prose">
            {@html marked(m.math_mdl_sir_implementation_modelbase_2())}
          </div>
          <pre class="code-block"><code>{sirV2Model}</code></pre>
          <div class="prose">
            {@html marked(m.math_mdl_sir_implementation_modelbase_3())}
          </div>
          <pre class="code-block"><code>{sirV2Reactions}</code></pre>
          <div class="prose">
            {@html marked(m.math_mdl_sir_implementation_modelbase_4())}
          </div>
          <figure class="page-figure">
            <img
              src="{base}/pictures/SIR_modelbase.png"
              alt="SIR modelbase plot"
              class="page-img half-width"
            />
          </figure>
          <pre class="code-block"><code>{sirV2Simulation}</code></pre>
          <div class="prose">
            {@html marked(m.math_mdl_sir_implementation_modelbase_5())}
          </div>
          <pre class="code-block"><code>{sird}</code></pre>
          <div class="prose">
            {@html marked(m.math_mdl_sir_implementation_modelbase_6())}
          </div>
        {/if}
      </div>
    </div>
  </section>

  <div class="prose">
    {@html marked(m.mdl_link_plants_and_python())}
  </div>

  <section>
    <div class="prose">
      {@html marked(m.mdl_headline_model_photosynthesis())}
      {@html marked(m.mdl_models_overview())}
    </div>

    <!-- Photosynthesis model tabs -->
    <div class="accordion">
      <Expander title={m.mdl_headline_fvcb()}>
        <div class="prose">
          {@html marked(ta(m.bio_mdl_fvcb_1(), m.math_mdl_fvcb_1()))}
          {@html marked(ta(m.bio_mdl_fvcb_2(), m.math_mdl_fvcb_2()))}
        </div>
        {#if audienceStore.audience === "4math"}
          <div class="katex-block">
            <Katex displayMode
              >{"\\newcommand{\\indexni}[2]{#1 _{\\mathrm{#2}}} \\newcommand{\\indexnig}[2]{\\mathit{#1} _{\\mathrm{#2}}} \\begin{aligned} \\indexni{A}{c} &= \\frac{(\\indexni{C}{c} - \\indexnig{\\Gamma}{*}) \\cdot \\indexni{V}{cmax}}{\\indexni{C}{c} + \\indexni{K}{c} \\cdot \\left(1+ \\dfrac{O}{\\indexni{K}{o}}\\right)} - \\indexni{R}{d}\\\\ \\indexni{A}{j} &= \\dfrac{\\left(\\indexni{C}{c} - \\indexnig{\\Gamma}{*}\\right)\\cdot J}{4 \\cdot \\indexni{C}{c} + 8\\cdot\\indexnig{\\Gamma}{*}} - \\indexni{R}{d}\\\\ \\indexni{A}{p} &= 3\\cdot \\indexni{T}{p} - \\indexni{R}{d}\\\\ A &= \\mathrm{min}\\left(\\indexni{A}{c},\\ \\indexni{A}{j},\\ \\indexni{A}{p}\\right) \\end{aligned}"}</Katex
            >
          </div>
        {/if}
        <div class="prose">
          {@html marked(ta(m.bio_mdl_fvcb_3(), m.math_mdl_fvcb_3()))}
          {@html marked(ta(m.bio_mdl_fvcb_4(), m.math_mdl_fvcb_4()))}
        </div>
        {#if audienceStore.audience === "4math"}
          <div class="prose">
            {@html marked(m.math_mdl_fvcb_5())}
          </div>
        {/if}
      </Expander>

      <Expander title={m.mdl_headline_e_photosynthesis()}>
        <div class="prose">
          {@html marked(
            ta(m.bio_mdl_e_photosynthesis_1(), m.math_mdl_e_photosynthesis_1()),
          )}
          {@html marked(
            ta(m.bio_mdl_e_photosynthesis_2(), m.math_mdl_e_photosynthesis_2()),
          )}
          {@html marked(
            ta(m.bio_mdl_e_photosynthesis_3(), m.math_mdl_e_photosynthesis_3()),
          )}
        </div>
      </Expander>

      <Expander title={m.mdl_headline_bellasio()}>
        <div class="prose">
          {@html marked(ta(m.bio_mdl_bellasio_1(), m.math_mdl_bellasio_1()))}
          {@html marked(ta(m.bio_mdl_bellasio_2(), m.math_mdl_bellasio_2()))}
          {@html marked(ta(m.bio_mdl_bellasio_3(), m.math_mdl_bellasio_3()))}
          {@html marked(ta(m.bio_mdl_bellasio_4(), m.math_mdl_bellasio_4()))}
        </div>
      </Expander>
    </div>

    <Expander
      title={ta(m.bio_mdl_expander_c3c4cam(), m.math_mdl_expander_c3c4cam())}
    >
      <div class="prose">
        <div>{@html m.mdl_headline_c3()}</div>
        <div>{@html m.mdl_c3_1()}</div>
        <div>{@html m.mdl_headline_c4()}</div>
        <div>{@html m.mdl_c4_1()}</div>
        <div>{@html m.mdl_headline_cam()}</div>
        <div>{@html ta(m.bio_mdl_cam_1(), m.math_mdl_cam_1())}</div>
      </div>
    </Expander>
  </section>

  <Expander title={m.literature()}>
    <div class="prose">
      <p>{m.literature_onpage()}</p>
      <ol>
        <li>
          van Aalst, M., Ebenhöh, O., &amp; Matuszyńska, A. (2021). Constructing
          and analysing dynamic models with modelbase v1.2.3. BMC
          Bioinformatics, 22(1), 1-15.
          <a href="https://doi.org/10.1186/s12859-021-04122-7">
            https://doi.org/10.1186/s12859-021-04122-7
          </a>
        </li>
        <li>
          Farquhar, G. D., von Caemmerer, S., &amp; Berry, J. A. (1980). A
          biochemical model of photosynthetic CO₂ assimilation in leaves of C3
          species. Planta, 149(1), 78-90.
          <a href="https://doi.org/10.1007/BF00386231"
            >https://doi.org/10.1007/BF00386231</a
          >
        </li>
        <li>
          Von Caemmerer, S. (2013). Steady-state models of photosynthesis.
          Plant, Cell &amp; Environment, 36(9), 1617-1630.
          <a href="https://doi.org/10.1111/pce.12098"
            >https://doi.org/10.1111/pce.12098</a
          >
        </li>
        <li>
          Zhu, X.-G., Wang, Y., Ort, D. R., &amp; Long, S. P. (2013).
          e-photosynthesis. Plant, Cell &amp; Environment, 36(9), 1711-1727.
          <a href="https://doi.org/10.1111/pce.12025"
            >https://doi.org/10.1111/pce.12025</a
          >
        </li>
        <li>
          Bellasio, C. (2019). A generalised dynamic model of leaf-level C3
          photosynthesis. Photosynthesis Research, 141(1), 99-118.
          <a href="https://doi.org/10.1007/s11120-018-0601-1">
            https://doi.org/10.1007/s11120-018-0601-1
          </a>
        </li>
      </ol>
      <p>{@html marked(m.literature_plants_and_python())}</p>
    </div>
  </Expander>

  <PageNav
    base={base}
    prev={{ href: "/method", label: m.sde_pagenames_measuringmethod() }}
    next={{
      href: "/experiments",
      label: m.sde_pagenames_experimentsinsilico(),
    }}
  />
</article>

<style>
  section {
    margin: var(--space-8) 0;
  }

  .page-img.half-width {
    display: block;
    margin: 0 auto;
    max-width: 50%;
  }

  .caption {
    margin-top: var(--space-2);
    color: var(--color-text-muted);
    font-size: 0.875rem;
    text-align: center;
  }

  /* Tabs */
  .tabs {
    margin: var(--space-6) 0;
  }

  .tab-list {
    display: flex;
    gap: var(--space-1);
    margin-bottom: 0;
    border-bottom: 2px solid var(--color-border);
  }

  .tab-list button {
    transition:
      color 0.15s,
      border-color 0.15s;
    cursor: pointer;
    margin-bottom: -2px;
    border: none;
    border-bottom: 2px solid transparent;
    background: none;
    padding: var(--space-2) var(--space-4);
    color: var(--color-text-muted);
    font-weight: 500;
    font-size: 0.9rem;
  }

  .tab-list button:hover {
    color: var(--color-text);
  }

  .tab-list button.active {
    border-bottom-color: var(--color-primary);
    color: var(--color-primary);
  }

  .tab-panel {
    border: 1px solid var(--color-border);
    border-top: none;
    border-radius: 0 0 6px 6px;
    background: var(--color-bg);
    padding: var(--space-6);
  }

  /* KaTeX equations */
  .katex-block {
    margin: var(--space-4) 0;
    border-radius: 6px;
    background: var(--color-surface);
    padding: var(--space-4);
    overflow-x: auto;
  }

  /* Code blocks */
  .code-block {
    margin: var(--space-4) 0;
    border-radius: 6px;
    background: #1e1e1e;
    padding: var(--space-4);
    overflow-x: auto;
    color: #d4d4d4;
    font-size: 0.85rem;
    line-height: 1.5;
    font-family: var(--font-mono);
    white-space: pre;
  }

  .accordion {
    margin: var(--space-4) 0;
  }
</style>
