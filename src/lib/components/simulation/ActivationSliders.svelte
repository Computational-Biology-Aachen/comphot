<script lang="ts">
	import * as m from '$lib/paraglide/messages';

	interface Props {
		activationIdx: number;
		deactivationIdx: number;
		activationMultiplier: number;
		deactivationMultiplier: number;
	}

	let {
		activationIdx = $bindable(),
		deactivationIdx = $bindable(),
		activationMultiplier,
		deactivationMultiplier
	}: Props = $props();
</script>

<label class="slider-label">
	{@html m.slider_activation()}: <strong>{activationMultiplier}</strong>
	<input type="range" min="0" max="20" step="1" bind:value={activationIdx} />
</label>
<label class="slider-label">
	{@html m.slider_deactivation()}: <strong>{deactivationMultiplier}</strong>
	<input type="range" min="0" max="20" step="1" bind:value={deactivationIdx} />
</label>
