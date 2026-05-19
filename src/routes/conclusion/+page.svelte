<script lang="ts">
  import { base } from "$app/paths";
  import { ta } from "$lib/i18n";
  import * as m from "$lib/paraglide/messages";
  import {
    H1,
    Main,
    Narrow,
    PageNav,
    Text,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";
</script>

<svelte:head>
  <title>{m.con_headline_conclusion()} | ComPhot</title>
</svelte:head>

<Main>
  <Narrow>
    <H1>{@html marked(m.con_headline_conclusion())}</H1>
    <PageNav
      base={base}
      prev={{
        href: "/plant-memory",
        label: m.sde_pagenames_plantlightmemory(),
      }}
      next={{ href: "/contact", label: m.sde_pagenames_contact() }}
    />

    <Text>
      {@html marked(
        ta(m.bio_con_conclusion_text_one(), m.math_con_conclusion_text_one()),
      )}
    </Text>

    <figure>
      <img
        src="{base}/pictures/photosynthesis_productivity.gif"
        alt="Photosynthesis productivity animation"
        class="page-img centered"
      />
    </figure>

    <Text>
      {@html marked(m.con_conclusion_text_two())}
    </Text>

    <PageNav
      base={base}
      prev={{
        href: "/plant-memory",
        label: m.sde_pagenames_plantlightmemory(),
      }}
      next={{ href: "/contact", label: m.sde_pagenames_contact() }}
    />
  </Narrow>
</Main>
