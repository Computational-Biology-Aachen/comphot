<script lang="ts">
	import { Accordion as Expander } from '@computational-biology-aachen/design';
	import * as m from '$lib/paraglide/messages';
	import { marked } from 'marked';
</script>

<Expander title={m.literature()}>
	<p>{@html marked(m.literature_onpage())}</p>
	<ul>
		<li>
			Matuszyńska, A., Heidari, S., Jahns, P., &amp; Ebenhöh, O. (2016). A mathematical model of
			non-photochemical quenching to study short-term light memory in plants.
			<em>Biochimica et Biophysica Acta (BBA) - Bioenergetics</em>, 1857(12), 1860-1869.
			<a href="https://doi.org/10.1016/j.bbabio.2016.09.003" target="_blank" rel="noopener"
				>https://doi.org/10.1016/j.bbabio.2016.09.003</a
			>
		</li>
	</ul>
</Expander>
