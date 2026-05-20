<script lang="ts">
  import { getLocale, setLocale } from "$lib/paraglide/runtime";

  let {
    locales,
  }: {
    locales: { code: string; label: string }[];
  } = $props();

  let currentLocale = $state(getLocale());

  function switchLocale(code: (typeof locales)[number]["code"]) {
    setLocale(code);
    currentLocale = getLocale();
  }
</script>

<div class="lang-switcher">
  {#each locales as { code, label } (code)}
    <button
      class="lang-btn"
      class:active={currentLocale === code}
      onclick={() => switchLocale(code)}
    >
      {label}
    </button>
  {/each}
</div>

<style>
  .lang-switcher {
    display: flex;
    gap: 2px;
  }

  .lang-btn {
    transition:
      color 0.15s,
      background 0.15s,
      border-color 0.15s;
    cursor: pointer;
    border: 1px solid var(--color-border);
    border-radius: 4px;
    background: transparent;
    padding: 3px 8px;
    color: var(--color-text-muted);
    font-weight: 500;
    font-size: 0.8rem;
    line-height: 1;
  }

  .lang-btn:hover {
    border-color: var(--color-text-muted);
    color: var(--color-text);
  }

  .lang-btn.active {
    border-color: var(--color-primary);
    background: var(--color-primary);
    color: #fff;
  }
</style>
