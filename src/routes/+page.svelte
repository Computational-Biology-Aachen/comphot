<script lang="ts">
  import { base } from "$app/paths";
  import { ta } from "$lib/i18n";
  import * as m from "$lib/paraglide/messages";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import {
    Accordion,
    H1,
    H2,
    Image,
    InfoBox,
    Li,
    Link,
    SectionMain as Main,
    Ol,
    PageNav,
    Section,
    Text,
    Ul,
    YouTubeEmbed,
  } from "@computational-biology-aachen/design";
  import { faGithub } from "@fortawesome/free-brands-svg-icons";
  import { marked } from "marked";
  import Fa from "svelte-fa";
</script>

<Main
  width="90ch"
  align="start"
>
  <H1>
    {@html marked.parseInline(m.str_headline_main())}
  </H1>
  <Text>
    {@html marked.parseInline(m.str_intro())}
  </Text>

  <H2>
    {@html marked.parseInline(m.str_headline_usage())}
  </H2>
  <Text>
    {@html marked.parseInline(ta(m.bio_str_usage(), m.math_str_usage()))}
  </Text>
  <YouTubeEmbed
    videoId="KvyjIWLD8rU"
    title="Introduction video"
  />

  <Text>
    {@html marked.parseInline(
      ta(m.bio_str_specific_use(), m.math_str_specific_use()),
    )}
  </Text>

  <H2>
    {@html marked.parseInline(
      ta(
        m.bio_str_learning_objectives_header(),
        m.math_str_learning_objectives_header(),
      ),
    )}
  </H2>

  <InfoBox header="Learning objectives">
    {#if audienceStore.audience === "4math"}
      <Ul>
        <Li>{@html marked.parseInline(m.math_str_lo_1())}</Li>
        <Li>{@html marked.parseInline(m.math_str_lo_2())}</Li>
        <Li>{@html marked.parseInline(m.math_str_lo_3())}</Li>
        <Li>{@html marked.parseInline(m.math_str_lo_4())}</Li>
        <Li>{@html marked.parseInline(m.math_str_lo_5())}</Li>
      </Ul>
    {:else}
      <Ul>
        <Li>{@html marked.parseInline(m.bio_str_lo_1())}</Li>
        <Li>{@html marked.parseInline(m.bio_str_lo_2())}</Li>
        <Li>{@html marked.parseInline(m.bio_str_lo_3())}</Li>
        <Li>{@html marked.parseInline(m.bio_str_lo_4())}</Li>
      </Ul>
    {/if}
  </InfoBox>

  <Text>
    {@html marked.parseInline(m.str_link_plants_and_python())}
  </Text>

  <H2>{@html marked.parseInline(m.str_headline_pages())}</H2>
  <Text>
    {@html marked.parseInline(
      ta(m.bio_str_introduction_pages(), m.math_str_introduction_pages()),
    )}
    {@html marked.parseInline(
      ta(m.bio_str_photosynthesis(), m.math_str_photosynthesis()),
    )}
    {@html marked.parseInline(ta(m.bio_str_method(), m.math_str_method()))}
    {@html marked.parseInline(ta(m.bio_str_model(), m.math_str_model()))}
    {@html marked.parseInline(
      ta(m.bio_str_experiment(), m.math_str_experiment()),
    )}
    {@html marked.parseInline(ta(m.bio_str_memory(), m.math_str_memory()))}
  </Text>

  {#if audienceStore.audience === "4math"}
    <Text>
      {@html marked.parseInline(m.str_drop_box_intro())}
    </Text>
    <Accordion title={m.str_expander_in()}>
      <Text>
        {@html marked.parseInline(m.str_explanation_in_vitro())}
        {@html marked.parseInline(m.str_explanation_in_vivo())}
        {@html marked.parseInline(m.str_explanation_in_silico())}
      </Text>
    </Accordion>
  {/if}

  <Accordion title={m.str_expander_about()}>
    <Text>
      {@html marked.parseInline(m.str_explanation_about())}
    </Text>
  </Accordion>

  <Accordion title={m.appearances()}>
    <Text>
      {@html marked.parseInline(m.appearance_explanation())}
      {@html marked.parseInline(m.eps2_conference_title())}
      {@html marked.parseInline(m.eps2_conference_1())}
      {@html marked.parseInline(m.eps2_conference_2())}
      {@html marked.parseInline(m.eps2_conference_3())}
    </Text>
    <Image
      src="{base}/pictures/Poster.png"
      alt="ComPhot Poster"
    />
    <Image
      src="{base}/pictures/Editable/Elouen_Poster.svg"
      alt="Elouen Poster"
    />
  </Accordion>

  <Accordion title={m.literature()}>
    <Text>
      {m.literature_onpage()}
    </Text>
    <Ol>
      <Li>
        Matuszyńska, A., Heidari, S., Jahns, P., &amp; Ebenhöh, O. (2016). A
        mathematical model of non-photochemical quenching to study short-term
        light memory in plants. Biochimica et Biophysica Acta (BBA) -
        Bioenergetics, 1857(12), 1860-1869.
        <Link href="https://doi.org/10.1016/j.bbabio.2016.09.003">
          https://doi.org/10.1016/j.bbabio.2016.09.003
        </Link>
      </Li>
    </Ol>
    <Text
      >{@html marked.parseInline(m.literature_plants_and_python_intro())}</Text
    >
    <Ul>
      <Li>{@html marked.parseInline(m.literature_plants_and_python_item1())}</Li
      >
      <Li>{@html marked.parseInline(m.literature_plants_and_python_item2())}</Li
      >
    </Ul>
  </Accordion>

  <PageNav
    base={base}
    next={{
      href: "/photosynthesis",
      label: m.sde_pagenames_photosynthesis(),
    }}
  />
</Main>

<Section
  variant="dark"
  width="full"
>
  <H2>Imprint</H2>
  <Text color="light">
    Anbieter i.S.d. TDG/MDStV: Prof. Dr. Anna B. Matuszyńska <br />
    Worringerweg 1 52074 Aachen <br />
    Sammelbau Biologie, Bauteil 42 C, Erdgeschoss, Raum 041 <br />
    Work Phone: +49 241 80 25817 <br />

    Verantwortlich i.S.d. § 6 Abs. 2 MDStV: <br />
    Prof. Dr. Anna B. Matuszyńska <br />
    Design und Umsetzung Dr. Marvin van Aalst <Link
      color="light"
      href="https://github.com/Computational-Biology-Aachen/comphot"
      ><Fa icon={faGithub} /></Link
    >
    <br />
    (c) 2025 Prof. Dr. Anna B. Matuszyńska, Alle Rechte vorbehalten.
  </Text>
</Section>
