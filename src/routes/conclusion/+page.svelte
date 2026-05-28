<script lang="ts">
  import { base } from "$app/paths";
  import * as m from "$lib/paraglide/messages";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import {
    Bold,
    H1,
    Li,
    SectionMain as Main,
    PageNav,
    Text,
    Ol,
    Ul,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";
</script>

<svelte:head>
  <title>{m.con_headline_conclusion()} | ComPhot</title>
</svelte:head>

<Main
  width="narrow"
  align="start"
>
  <H1>{@html marked.parseInline(m.con_headline_conclusion())}</H1>
  <PageNav
    base={base}
    prev={{
      href: "/plant-memory",
      label: m.sde_pagenames_plantlightmemory(),
    }}
    next={{ href: "/contact", label: m.sde_pagenames_contact() }}
  />

  <Text>
    {#if audienceStore.audience === "4bio"}
      {@html marked.parseInline(m.bio_con_conclusion_intro())}
    {:else}
      {@html marked.parseInline(m.math_con_conclusion_intro())}
    {/if}
  </Text>
  <Ul>
    <Li>{@html marked.parseInline(m.con_conclusion_c1())}</Li>
    {#if audienceStore.audience === "4bio"}
      <Li>{@html marked.parseInline(m.bio_con_conclusion_c2())}</Li>
    {:else}
      <Li>{@html marked.parseInline(m.math_con_conclusion_c2())}</Li>
    {/if}
  </Ul>

  <figure>
    <img
      src="{base}/pictures/photosynthesis_productivity.gif"
      alt="Photosynthesis productivity animation"
      class="page-img centered"
    />
  </figure>

  <Ul>
    <Li>{@html marked.parseInline(m.con_conclusion_c3())}</Li>
    <Li>{@html marked.parseInline(m.con_conclusion_c4())}</Li>
  </Ul>
  <Text>{@html marked.parseInline(m.con_conclusion_p1())}</Text>
  <Text>{@html marked.parseInline(m.con_conclusion_p2())}</Text>
  <Text><Bold>{@html marked.parseInline(m.con_conclusion_p3())}</Bold></Text>

  <PageNav
    base={base}
    prev={{
      href: "/plant-memory",
      label: m.sde_pagenames_plantlightmemory(),
    }}
    next={{ href: "/contact", label: m.sde_pagenames_contact() }}
  />
</Main>
