<script lang="ts">
  import { base } from "$app/paths";
  import { page } from "$app/state";
  import favicon from "$lib/assets/cpbl-favicon.svg";
  import * as config from "$lib/config";
  import * as m from "$lib/paraglide/messages";
  import { locales, localizeHref } from "$lib/paraglide/runtime";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import {
    Navbar,
    NavGH,
    NavItem,
    Sidebar2 as Sidebar,
    LanguageSwitcher as ToggleLanguage,
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

  <NavGH href="https://github.com/Computational-Biology-Aachen/comphot" />
</Navbar>

<div class="two-col">
  <Sidebar
    navLinks={[
      { href: "/", label: "Home" },
      { href: "{base}/photosynthesis", label: "Photosynthesis" },
      { href: "{base}/method", label: "Method" },
      { href: "{base}/model", label: "Model" },
      { href: "{base}/experiments", label: "Experiments" },
      { href: "{base}/plant-memory", label: "Plant Memory" },
      { href: "{base}/conclusion", label: "Conclusion" },
      { href: "{base}/contact", label: "Contact" },
    ]}
    audienceOptions={[
      { value: "4bio", label: "4bio" },
      { value: "4math", label: "4math" },
    ]}
    audienceStore={audienceStore}
  >
    <ToggleLanguage
      locales={[
        { code: "en", label: "EN" },
        { code: "de", label: "DE" },
        { code: "fr", label: "FR" },
      ]}
    />
  </Sidebar>
  {@render children()}
</div>

<style>
  .brand {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    color: var(--color-primary);
    font-weight: 600;
  }

  .two-col {
    display: grid;
    grid-template-columns: 15rem auto;
  }
</style>
