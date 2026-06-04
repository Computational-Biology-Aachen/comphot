<script lang="ts">
  import { base } from "$app/paths";
  import { ta } from "$lib/i18n";
  import * as m from "$lib/paraglide/messages";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import {
    Accordion,
    Bold,
    Code,
    Figure,
    H1,
    H2,
    InfoBox,
    Li,
    Link,
    SectionMain as Main,
    Math,
    Ol,
    PageNav,
    Pre,
    Tabs,
    Text,
    Ul,
    YouTubeEmbed,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";

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

  const sirTabs = $derived(
    audienceStore.audience === "4math"
      ? [
          { key: "sir", label: m.mdl_tab_sir() },
          { key: "manual", label: m.math_mdl_tab_manual() },
          { key: "modelbase", label: m.math_mdl_tab_modelbase() },
        ]
      : [{ key: "sir", label: m.mdl_tab_sir() }],
  );
</script>

<svelte:head>
  <title>{m.mdl_headline_computational_models()} - ComPhot</title>
</svelte:head>

<Main
  width="90ch"
  align="start"
>
  <H1>
    {@html marked.parseInline(m.mdl_headline_computational_models())}
  </H1>

  <!-- section: learning objectives -->
  <InfoBox header="Learning objectives">
    {#if audienceStore.audience === "4math"}
      <Ul>
        <Li>{@html marked.parseInline(m.math_mdl_lo_1())}</Li>
        <Li>{@html marked.parseInline(m.math_mdl_lo_2())}</Li>
        <Li>{@html marked.parseInline(m.math_mdl_lo_3())}</Li>
      </Ul>
    {:else}
      <Ul>
        <Li>{@html marked.parseInline(m.bio_mdl_lo_1())}</Li>
        <Li>{@html marked.parseInline(m.bio_mdl_lo_2())}</Li>
      </Ul>
    {/if}
  </InfoBox>

  <InfoBox
    header="What you need to know"
    variant="warning"
  >
    {#if audienceStore.audience === "4math"}
      <Ul>
        <Li>{@html marked.parseInline(m.math_mdl_prereq_1())}</Li>
        <Li>{@html marked.parseInline(m.math_mdl_prereq_2())}</Li>
      </Ul>
    {:else}
      <Ul>
        <Li>{@html marked.parseInline(m.bio_mdl_prereq_1())}</Li>
        <Li>{@html marked.parseInline(m.bio_mdl_prereq_2())}</Li>
      </Ul>
    {/if}
  </InfoBox>

  <PageNav
    base={base}
    prev={{ href: "/method", label: m.sde_pagenames_measuringmethod() }}
    next={{
      href: "/experiments",
      label: m.sde_pagenames_experimentsinsilico(),
    }}
  />

  <H2>
    {@html marked.parseInline(m.mdl_headline_model())}
  </H2>
  <Text>
    {@html marked.parseInline(m.mdl_mathematical_modelling_explanation_1())}
  </Text>

  <Figure
    src="{base}/pictures/Modeling_scheme_eng.png"
    alt="Modeling cycle diagram"
  >
    {#snippet caption()}{m.mdl_caption_modelling_picture()}{/snippet}
  </Figure>

  <Text>
    {@html marked.parseInline(m.mdl_mathematical_modelling_explanation_1b())}
  </Text>

  <YouTubeEmbed
    videoId="oVME5KIHrO8"
    title="Building mathematical models"
  />

  <H2>
    {@html marked.parseInline(m.mdl_example_mathematical_model())}
  </H2>

  <!-- Tabbed SIR section -->
  <Tabs tabs={sirTabs}>
    {#snippet children(activeKey)}
      {#if activeKey === "sir"}
        <Text>
          {@html marked.parseInline(m.mdl_headline_sir())}
          {@html marked.parseInline(
            ta(
              m.bio_mdl_mathematical_modelling_example(),
              m.math_mdl_mathematical_modelling_example(),
            ),
          )}
        </Text>

        {#if audienceStore.audience === "4bio"}
          <div class="max-width">
            <Figure
              src="{base}/pictures/SIR_Aliens.png"
              alt="SIR Aliens diagram"
            />
          </div>
        {:else}
          <Math
            tex={"\\mathrm{S} \\xrightarrow{\\textit{v}_1} \\mathrm{I} \\xrightarrow{\\textit{v}_2} \\mathrm{R}"}
            display
          ></Math>
          <Math
            tex={"\\begin{aligned} v_1 &= \\beta \\cdot \\frac{\\mathrm{S}\\cdot \\mathrm{I}}{\\mathrm{N}} \\\\ v_2 &= \\gamma \\cdot \\mathrm{I} \\\\ \\end{aligned}"}
            display
          ></Math>
        {/if}

        <Text>
          {@html marked.parseInline(
            ta(
              m.bio_mdl_mathematical_modelling_example_1(),
              m.math_mdl_mathematical_modelling_example_1(),
            ),
          )}
        </Text>

        {#if audienceStore.audience === "4bio"}
          <div class="max-width">
            <Figure
              src="{base}/pictures/SIR_AliensScheme.png"
              alt="SIR Aliens scheme"
            />
          </div>
        {:else}
          <Math
            tex={"\\mathrm{S} \\xrightarrow{\\textit{v}_1} \\mathrm{I} \\xrightarrow{\\textit{v}_2} \\mathrm{R}"}
            display
          ></Math>
          <Math
            tex={"\\begin{aligned} \\frac{\\mathrm{d}\\mathrm{S}}{\\mathrm{d}t} &= - v_1 \\\\ \\frac{\\mathrm{d}\\mathrm{I}}{\\mathrm{d}t} &= v_1 - v_2 \\\\ \\frac{\\mathrm{d}\\mathrm{R}}{\\mathrm{d}t} &= v_2 \\end{aligned}"}
            display
          ></Math>
        {/if}

        <Text>
          {@html marked.parseInline(
            ta(
              m.bio_mdl_mathematical_modelling_example_2(),
              m.math_mdl_mathematical_modelling_example_2(),
            ),
          )}
        </Text>

        {#if audienceStore.audience === "4bio"}
          <Math
            tex={"\\begin{aligned} \\mathrm{Infecting\\ rate:\\ } v_1 &= \\beta \\cdot \\frac{\\mathrm{S}\\cdot \\mathrm{I}}{\\mathrm{N}} \\\\ \\mathrm{Recovery\\ rate:\\ } v_{2} &= \\gamma \\cdot \\mathrm{I} \\\\ \\end{aligned}"}
            display
          ></Math>
          <Text>
            {@html marked.parseInline(
              m.bio_mdl_mathematical_modelling_example_3(),
            )}
          </Text>
          <Math
            tex={"\\begin{aligned} \\mathrm{dS} &= -v_1 \\cdot \\mathrm{d}t \\\\ \\mathrm{dI} &= \\left( v_1 - v_2 \\right) \\cdot \\mathrm{d}t \\\\ \\mathrm{dR} &= v_2 \\cdot \\mathrm{d}t \\end{aligned}"}
            display
          ></Math>

          <Text>
            {@html marked.parseInline(
              m.bio_mdl_mathematical_modelling_example_4(),
            )}
          </Text>
        {/if}

        <Text>
          {@html marked.parseInline(
            ta(
              m.bio_mdl_mathematical_modelling_example_simple(),
              m.math_mdl_mathematical_modelling_example_simple(),
            ),
          )}
        </Text>
      {:else if activeKey === "manual"}
        <Text>
          {@html marked.parseInline(m.math_mdl_headline_manual())}
        </Text>
        <Code><Pre>{sirV1Integ}</Pre></Code>
        <Text>
          {@html marked.parseInline(m.math_mdl_sir_implementation_manual_1())}
        </Text>
        <Figure
          src="{base}/pictures/SIR_manual.png"
          alt="SIR model manual plot"
        />
        <Code><Pre>{sirV1Plot}</Pre></Code>
        <Text>
          {@html marked.parseInline(m.math_mdl_sir_implementation_manual_2())}
        </Text>
      {:else if activeKey === "modelbase"}
        <Text>
          {@html marked.parseInline(m.math_mdl_headline_modelbase())}
          {@html marked.parseInline(
            m.math_mdl_sir_implementation_modelbase_1(),
          )}
        </Text>
        <Code><Pre>{sirV2RateFns}</Pre></Code>
        <Text>
          {@html marked.parseInline(
            m.math_mdl_sir_implementation_modelbase_2(),
          )}
        </Text>
        <Code><Pre>{sirV2Model}</Pre></Code>
        <Text
          >{@html marked.parseInline(
            m.math_mdl_sir_implementation_modelbase_3_intro(),
          )}</Text
        >
        <Ol>
          <Li>{m.math_mdl_sir_implementation_modelbase_3_item1()}</Li>
          <Li>{m.math_mdl_sir_implementation_modelbase_3_item2()}</Li>
          <Li>{m.math_mdl_sir_implementation_modelbase_3_item3()}</Li>
          <Li>{m.math_mdl_sir_implementation_modelbase_3_item4()}</Li>
        </Ol>
        <Code><Pre>{sirV2Reactions}</Pre></Code>
        <Text>
          {@html marked.parseInline(
            m.math_mdl_sir_implementation_modelbase_4(),
          )}
        </Text>
        <Figure
          src="{base}/pictures/SIR_modelbase.png"
          alt="SIR modelbase plot"
        />
        <Code><Pre>{sirV2Simulation}</Pre></Code>
        <Text>
          {@html marked.parseInline(
            m.math_mdl_sir_implementation_modelbase_5(),
          )}
        </Text>
        <Code><Pre>{sird}</Pre></Code>
        <Text>
          {@html marked.parseInline(
            m.math_mdl_sir_implementation_modelbase_6(),
          )}
        </Text>
      {/if}
    {/snippet}
  </Tabs>

  <Text>
    {@html marked.parseInline(m.mdl_link_plants_and_python())}
  </Text>

  <H2>
    {@html marked.parseInline(m.mdl_headline_model_photosynthesis())}
  </H2>
  <Text>
    {@html marked.parseInline(m.mdl_models_overview())}
  </Text>

  <!-- The Farquhar, von Caemmerer and Berry model -->
  <Accordion title={m.mdl_headline_fvcb()}>
    <Text>
      {@html marked.parseInline(ta(m.bio_mdl_fvcb_1(), m.math_mdl_fvcb_1()))}
      {@html marked.parseInline(ta(m.bio_mdl_fvcb_2(), m.math_mdl_fvcb_2()))}
    </Text>
    {#if audienceStore.audience === "4math"}
      <Math
        tex={"\\newcommand{\\indexni}[2]{#1 _{\\mathrm{#2}}} \\newcommand{\\indexnig}[2]{\\mathit{#1} _{\\mathrm{#2}}} \\begin{aligned} \\indexni{A}{c} &= \\frac{(\\indexni{C}{c} - \\indexnig{\\Gamma}{*}) \\cdot \\indexni{V}{cmax}}{\\indexni{C}{c} + \\indexni{K}{c} \\cdot \\left(1+ \\dfrac{O}{\\indexni{K}{o}}\\right)} - \\indexni{R}{d}\\\\ \\indexni{A}{j} &= \\dfrac{\\left(\\indexni{C}{c} - \\indexnig{\\Gamma}{*}\\right)\\cdot J}{4 \\cdot \\indexni{C}{c} + 8\\cdot\\indexnig{\\Gamma}{*}} - \\indexni{R}{d}\\\\ \\indexni{A}{p} &= 3\\cdot \\indexni{T}{p} - \\indexni{R}{d}\\\\ A &= \\mathrm{min}\\left(\\indexni{A}{c},\\ \\indexni{A}{j},\\ \\indexni{A}{p}\\right) \\end{aligned}"}
        display
      ></Math>
    {/if}
    <Text>
      {@html marked.parseInline(ta(m.bio_mdl_fvcb_3(), m.math_mdl_fvcb_3()))}
      {@html marked.parseInline(ta(m.bio_mdl_fvcb_4(), m.math_mdl_fvcb_4()))}
    </Text>
    {#if audienceStore.audience === "4math"}
      <Text>
        {@html marked.parseInline(m.math_mdl_fvcb_5())}
      </Text>
    {/if}
  </Accordion>

  <!-- The e-photosynthesis model -->
  <Accordion>
    {#snippet header()}
      {@html marked.parse(m.mdl_headline_e_photosynthesis())}
    {/snippet}
    <Text>
      {@html marked.parseInline(
        ta(m.bio_mdl_e_photosynthesis_1(), m.math_mdl_e_photosynthesis_1()),
      )}
      {@html marked.parseInline(
        ta(m.bio_mdl_e_photosynthesis_2(), m.math_mdl_e_photosynthesis_2()),
      )}
      {@html marked.parseInline(
        ta(m.bio_mdl_e_photosynthesis_3(), m.math_mdl_e_photosynthesis_3()),
      )}
    </Text>
  </Accordion>

  <Accordion title={m.mdl_headline_bellasio()}>
    <Text>
      {@html marked.parseInline(
        ta(m.bio_mdl_bellasio_1(), m.math_mdl_bellasio_1()),
      )}
      {@html marked.parseInline(
        ta(m.bio_mdl_bellasio_2(), m.math_mdl_bellasio_2()),
      )}
      {@html marked.parseInline(
        ta(m.bio_mdl_bellasio_3(), m.math_mdl_bellasio_3()),
      )}
      {@html marked.parseInline(
        ta(m.bio_mdl_bellasio_4(), m.math_mdl_bellasio_4()),
      )}
    </Text>
  </Accordion>

  <Accordion
    title={ta(m.bio_mdl_expander_c3c4cam(), m.math_mdl_expander_c3c4cam())}
  >
    <Bold>{@html m.mdl_headline_c3()}</Bold>
    <Text>{@html m.mdl_c3_1()}</Text>
    <Bold>{@html m.mdl_headline_c4()}</Bold>
    <Text>{@html m.mdl_c4_1()}</Text>
    <Bold>{@html m.mdl_headline_cam()}</Bold>
    <Text>{@html ta(m.bio_mdl_cam_1(), m.math_mdl_cam_1())}</Text>
  </Accordion>

  <Accordion title={m.literature()}>
    <Text>
      <Text>{m.literature_onpage()}</Text>
      <Ol>
        <Li>
          van Aalst, M., Ebenhöh, O., &amp; Matuszyńska, A. (2021). Constructing
          and analysing dynamic models with modelbase v1.2.3. BMC
          Bioinformatics, 22(1), 1-15.
          <Link href="https://doi.org/10.1186/s12859-021-04122-7">
            https://doi.org/10.1186/s12859-021-04122-7
          </Link>
        </Li>
        <Li>
          Farquhar, G. D., von Caemmerer, S., &amp; Berry, J. A. (1980). A
          biochemical model of photosynthetic CO₂ assimilation in leaves of C3
          species. Planta, 149(1), 78-90.
          <Link href="https://doi.org/10.1007/BF00386231"
            >https://doi.org/10.1007/BF00386231</Link
          >
        </Li>
        <Li>
          Von Caemmerer, S. (2013). Steady-state models of photosynthesis.
          Plant, Cell &amp; Environment, 36(9), 1617-1630.
          <Link href="https://doi.org/10.1111/pce.12098"
            >https://doi.org/10.1111/pce.12098</Link
          >
        </Li>
        <Li>
          Zhu, X.-G., Wang, Y., Ort, D. R., &amp; Long, S. P. (2013).
          e-photosynthesis. Plant, Cell &amp; Environment, 36(9), 1711-1727.
          <Link href="https://doi.org/10.1111/pce.12025"
            >https://doi.org/10.1111/pce.12025</Link
          >
        </Li>
        <Li>
          Bellasio, C. (2019). A generalised dynamic model of leaf-level C3
          photosynthesis. Photosynthesis Research, 141(1), 99-118.
          <Link href="https://doi.org/10.1007/s11120-018-0601-1">
            https://doi.org/10.1007/s11120-018-0601-1
          </Link>
        </Li>
      </Ol>
      <Text>
        {@html marked.parseInline(m.literature_plants_and_python_intro())}
      </Text>
      <Ul>
        <Li
          >{@html marked.parseInline(
            m.literature_plants_and_python_item1(),
          )}</Li
        >
        <Li
          >{@html marked.parseInline(
            m.literature_plants_and_python_item2(),
          )}</Li
        >
      </Ul>
    </Text>
  </Accordion>

  <PageNav
    base={base}
    prev={{ href: "/method", label: m.sde_pagenames_measuringmethod() }}
    next={{
      href: "/experiments",
      label: m.sde_pagenames_experimentsinsilico(),
    }}
  />
</Main>

<style>
  .max-width {
    margin: auto;
    max-width: 40rem;
  }
</style>
