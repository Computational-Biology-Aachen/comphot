<script lang="ts">
  import { base } from "$app/paths";
  import { page } from "$app/state";
  import favicon from "$lib/assets/cpbl-favicon.svg";
  import * as config from "$lib/config";
  import * as m from "$lib/paraglide/messages";
  import { locales, localizeHref } from "$lib/paraglide/runtime";
  import {
    ButtonMenu,
    ButtonMenuItem,
    Navbar,
    NavGH,
    NavItem,
  } from "@computational-biology-aachen/design";
  import "../app.css";

  let { children } = $props();

  // Get the route path without base prefix for localizeHref
  function routePath() {
    const routeId = page.route.id ?? "/";
    return routeId;
  }
</script>

<svelte:head>
  <meta
    name="description"
    content={config.description}
  />
  <meta
    property="og:title"
    content={config.title}
  />
  <meta
    property="og:description"
    content={config.description}
  />
  <meta
    property="og:url"
    content={config.url}
  />
  <meta
    property="og:type"
    content="website"
  />
  <meta
    name="twitter:card"
    content="summary"
  />
  <link
    rel="icon"
    href={favicon}
  />
  <title>{m.str_headline_main()} | ComPhot</title>
  <!-- Alternate locale links for crawlers -->
  {#each locales as locale (locale)}
    <link
      rel="alternate"
      hreflang={locale}
      href="{base}{localizeHref(routePath(), { locale })}"
    />
  {/each}
  <meta
    property="og:type"
    content="website"
  />
  <meta
    name="twitter:card"
    content="summary"
  />
</svelte:head>

<!-- Hidden locale links for Paraglide's prerender crawler -->
<div style="display:none">
  {#each locales as locale (locale)}
    <a href="{base}{localizeHref(routePath(), { locale })}">{locale}</a>
  {/each}
</div>

<Navbar>
  {#snippet brand()}
    <div class="brand">
      <span>ComPhot</span>
    </div>
  {/snippet}
  <NavItem href="{base}/">Home</NavItem>

  <NavItem href="{base}/photosynthesis">Photosynthesis</NavItem>
  <NavItem href="{base}/method">Method</NavItem>
  <NavItem href="{base}/model">Model</NavItem>
  <NavItem href="{base}/experiments">Experiments</NavItem>
  <NavItem href="{base}/plant-memory">Plant Memory</NavItem>
  <NavItem href="{base}/conclusion">Conclusion</NavItem>
  <NavItem href="{base}/contact">Contact</NavItem>
  <ButtonMenu label="">
    <ButtonMenuItem>4bio</ButtonMenuItem>
    <ButtonMenuItem>4math</ButtonMenuItem>
    <ButtonMenuItem>en</ButtonMenuItem>
    <ButtonMenuItem>de</ButtonMenuItem>
    <ButtonMenuItem>fr</ButtonMenuItem>
  </ButtonMenu>

  <NavGH href="https://github.com/Computational-Biology-Aachen/comphot" />
</Navbar>

{@render children()}

<style>
  .brand {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    color: var(--color-primary);
    font-weight: 600;
  }
</style>
