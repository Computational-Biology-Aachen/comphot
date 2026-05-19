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
    <a
      href="{base}/"
      class="brand">ComPhot</a
    >
  {/snippet}
  <NavGH href="https://github.com/Computational-Biology-Aachen/comphot" />
</Navbar>

<div class="two-col">
  <Sidebar
    navLinks={[
      { href: "/", label: "Home" },
      { href: "/photosynthesis", label: "Photosynthesis" },
      { href: "/method", label: "Method" },
      { href: "/model", label: "Model" },
      { href: "/experiments", label: "Experiments" },
      { href: "/plant-memory", label: "Plant Memory" },
      { href: "/conclusion", label: "Conclusion" },
      { href: "/contact", label: "Contact" },
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
    color: var(--color-primary);
    font-weight: 600;
    font-size: 1.2rem;
    letter-spacing: -0.01em;
    text-decoration: none;
  }

  .two-col {
    display: flex;
    flex-direction: row;
  }
</style>
