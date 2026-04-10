<script lang="ts">
	interface Props {
		checked?: boolean;
		label?: string;
		onchange?: (checked: boolean) => void;
	}

	let { checked = $bindable(true), label = 'Compare with last simulation', onchange }: Props =
		$props();
</script>

<label class="compare-label">
	<input
		type="checkbox"
		bind:checked
		onchange={() => onchange?.(checked)}
		class="compare-input"
	/>
	{label}
</label>

<style>
	.compare-label {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		cursor: pointer;
		font-size: 0.95rem;
		user-select: none;
	}

	.compare-input {
		width: 1.1em;
		height: 1.1em;
		cursor: pointer;
		accent-color: var(--color-primary);
	}
</style>
