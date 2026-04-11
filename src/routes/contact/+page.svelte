<script lang="ts">
	import { marked } from 'marked';
	import { resolve } from '$app/paths';
	import * as m from '$lib/paraglide/messages';
	import PageNav from '$lib/components/PageNav.svelte';
	import Expander from '$lib/components/Expander.svelte';

	const bibTexContent = `@article{,
 author = {Phillips, Sarah and Pfennig, Tobias and Corvest, Elouen and van Aalst, Marvin and Fürtauer, Lisa and Matuszyńska, Anna},
 year = {2024},
 title = {Computational Photosynthesis (ComPhot): Simulation-Based Learning Platform to Study Photosynthesis},
 journal = {The Plant Cell},
}`;

	const risContent = `TY  - JOUR
AU  - Phillips, Sarah
AU  - Pfennig, Tobias
AU  - Corvest, Elouen
AU  - Aalst, Marvin
AU  - Fürtauer, Lisa
AU  - Matuszyńska, Anna
T1  - Computational Photosynthesis (ComPhot): Simulation-Based Learning Platform to Study Photosynthesis
PY  - 2024
JO  - The Plant Cell
ER  -`;

	const endnoteContent = `%0 Journal Article
%T Computational Photosynthesis (ComPhot): Simulation-Based Learning Platform to Study Photosynthesis
%B The Plant Cell
%A Phillips, Sarah
%A Pfennig, Tobias
%A Corvest, Elouen
%A Aalst, Marvin van
%A Fürtauer, Lisa
%A Matuszyńska, Anna
%D 2024
%J The Plant Cell`;

	let selectedFormat = $state<'BibTeX' | 'RIS' | 'EndNote' | null>(null);

	function getCiteContent() {
		if (selectedFormat === 'BibTeX') return bibTexContent;
		if (selectedFormat === 'RIS') return risContent;
		if (selectedFormat === 'EndNote') return endnoteContent;
		return '';
	}

	function getDownloadFilename() {
		if (selectedFormat === 'BibTeX') return 'ComPhot.bib';
		if (selectedFormat === 'RIS') return 'ComPhot.ris';
		if (selectedFormat === 'EndNote') return 'ComPhot.enw';
		return '';
	}

	function downloadCite() {
		const content = getCiteContent();
		const filename = getDownloadFilename();
		const blob = new Blob([content], { type: 'text/plain' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = filename;
		a.click();
		URL.revokeObjectURL(url);
	}
</script>

<svelte:head>
	<title>{m.cont_header()} | ComPhot</title>
</svelte:head>

<article class="page-content">
	<h1 class="contact-header">
		<span class="mailbox-icon" aria-hidden="true">📬</span>
		{m.cont_header()}
	</h1>

	<PageNav prev={{ href: '/conclusion', label: m.sde_pagenames_conclusion() }} />

	<p class="subheader">{m.cont_subheader()}</p>

	<section class="team-section">
		<div class="team-card">
			<h3>Sarah Philipps</h3>
			<ul>
				<li><strong>{m.cont_email()}</strong> <a href="mailto:sarah.philipps@rwth-aachen.de">sarah.philipps@rwth-aachen.de</a></li>
				<li><strong>{m.cont_topics()}</strong> {m.cont_topics_sarah()}</li>
			</ul>
		</div>

		<div class="team-card">
			<h3>Tobias Pfennig</h3>
			<ul>
				<li><strong>{m.cont_email()}</strong> <a href="mailto:tobias.pfennig@rwth-aachen.de">tobias.pfennig@rwth-aachen.de</a></li>
				<li><strong>{m.cont_topics()}</strong> {m.cont_topics_tobias()}</li>
				<li>
					<strong>{m.cont_website()}</strong>
					<a href="https://www.cpbl.rwth-aachen.de/cms/CPBL/Die-Juniorprofessur/Unser/~wljpm/Tobias-Pfennig/" target="_blank" rel="noopener">RWTH Aachen</a>
				</li>
			</ul>
		</div>

		<div class="team-card">
			<h3>Elouen Corvest</h3>
			<ul>
				<li><strong>{m.cont_email()}</strong> <a href="mailto:elouen.corvest@rwth-aachen.de">elouen.corvest@rwth-aachen.de</a></li>
				<li><strong>{m.cont_topics()}</strong> {m.cont_topics_elouen()}</li>
				<li>
					<strong>{m.cont_website()}</strong>
					<a href="https://www.cpbl.rwth-aachen.de/cms/CPBL/Die-Juniorprofessur/Unser/~wljuk/Elouen-Corvest/lidx/1/" target="_blank" rel="noopener">RWTH Aachen</a>
				</li>
			</ul>
		</div>

		<div class="team-card">
			<h3>Marvin van Aalst</h3>
			<ul>
				<li><strong>{m.cont_email()}</strong> <a href="mailto:marvin.van.aalst@hhu.de">marvin.van.aalst@hhu.de</a></li>
				<li><strong>{m.cont_topics()}</strong> {m.cont_topics_marvin()}</li>
				<li>
					<strong>{m.cont_website()}</strong>
					<a href="https://www.qtb.hhu.de/" target="_blank" rel="noopener">Heinrich Heine University Duesseldorf</a>
				</li>
			</ul>
		</div>

		<div class="team-card">
			<h3>Lisa Fürtauer</h3>
			<ul>
				<li><strong>{m.cont_email()}</strong> <a href="mailto:lisa.fuertauer@bio3.rwth-aachen.de">lisa.fuertauer@bio3.rwth-aachen.de</a></li>
				<li><strong>{m.cont_topics()}</strong> {m.cont_topics_lisa()}</li>
				<li>
					<strong>{m.cont_website()}</strong>
					<a href="https://www.bio3.rwth-aachen.de/cms/BIO3/Das-Institut/~tcejj/Juniorprofessur-Molekulare-Systembiologi/" target="_blank" rel="noopener">RWTH Aachen</a>
				</li>
			</ul>
		</div>

		<div class="team-card">
			<h3>Anna Matuszyńska</h3>
			<ul>
				<li><strong>{m.cont_email()}</strong> <a href="mailto:anna.matuszynska@rwth-aachen.de">anna.matuszynska@rwth-aachen.de</a></li>
				<li><strong>{m.cont_topics()}</strong> {m.cont_topics_anna()}</li>
				<li>
					<strong>{m.cont_website()}</strong>
					<a href="https://www.cpbl.rwth-aachen.de/cms/CPBL/Die-Juniorprofessur/Unser/~ywkwc/Anna-Matuszy-324-ska/" target="_blank" rel="noopener">RWTH Aachen</a>
				</li>
			</ul>
		</div>
	</section>

	<p class="note">{m.cont_hours()}</p>
	<p class="thanks">{m.cont_thanks()}</p>

	<Expander title={m.cont_cite()}>
		<p class="cite-intro">
			Computational Photosynthesis (ComPhot): Simulation-Based Learning Platform to Study
			Photosynthesis, The Plant Cell, 2024
		</p>

		<div class="cite-format-selector">
			<label for="cite-format"><strong>{m.cont_style()}</strong></label>
			<select
				id="cite-format"
				onchange={(e) =>
					(selectedFormat = (e.currentTarget as HTMLSelectElement).value as
						| 'BibTeX'
						| 'RIS'
						| 'EndNote'
						| null)}
			>
				<option value="">-- select --</option>
				<option value="BibTeX">BibTeX</option>
				<option value="RIS">RIS</option>
				<option value="EndNote">EndNote</option>
			</select>
		</div>

		{#if selectedFormat}
			<div class="cite-actions">
				<button class="download-btn" onclick={downloadCite}>
					Download {getDownloadFilename()}
				</button>
			</div>
			<pre class="code-block">{getCiteContent()}</pre>
		{/if}
	</Expander>

	<div class="prose">
		{@html marked(m.cont_resources())}
		{@html marked(m.programs_used())}
	</div>

	<PageNav prev={{ href: '/conclusion', label: m.sde_pagenames_conclusion() }} />
</article>

<style>
	.page-content {
		max-width: var(--content-max-width);
	}

	.contact-header {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		font-size: 2rem;
		margin-bottom: var(--space-4);
	}

	.mailbox-icon {
		font-size: 1.5rem;
	}

	.subheader {
		font-size: 1.05rem;
		color: var(--color-text-muted);
		margin-bottom: var(--space-6);
	}

	.team-section {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--space-4);
		margin: var(--space-6) 0;
	}

	@media (max-width: 700px) {
		.team-section {
			grid-template-columns: 1fr;
		}
	}

	.team-card {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 8px;
		padding: var(--space-4);
	}

	.team-card h3 {
		margin: 0 0 var(--space-3) 0;
		font-size: 1.1rem;
		color: var(--color-text);
	}

	.team-card ul {
		list-style: none;
		padding: 0;
		margin: 0;
		font-size: 0.9rem;
		display: flex;
		flex-direction: column;
		gap: var(--space-1);
	}

	.team-card a {
		color: var(--color-primary);
		word-break: break-all;
	}

	.note {
		font-size: 0.9rem;
		color: var(--color-text-muted);
		margin: var(--space-4) 0;
		font-style: italic;
	}

	.thanks {
		font-weight: 500;
		margin-bottom: var(--space-6);
	}

	.cite-intro {
		font-style: italic;
		margin-bottom: var(--space-4);
		padding: var(--space-3);
		background: var(--color-surface);
		border-radius: 4px;
	}

	.cite-format-selector {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		margin-bottom: var(--space-4);
	}

	.cite-format-selector select {
		padding: var(--space-2) var(--space-3);
		border: 1px solid var(--color-border);
		border-radius: 4px;
		background: var(--color-bg);
		font-size: 0.9rem;
	}

	.cite-actions {
		margin-bottom: var(--space-3);
	}

	.download-btn {
		padding: var(--space-2) var(--space-4);
		background: var(--color-primary);
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.9rem;
		transition: opacity 0.15s;
	}

	.download-btn:hover {
		opacity: 0.85;
	}

	.code-block {
		background: #1e1e1e;
		color: #d4d4d4;
		padding: var(--space-4);
		border-radius: 6px;
		overflow-x: auto;
		font-size: 0.85rem;
		line-height: 1.5;
		margin: var(--space-4) 0;
		font-family: var(--font-mono);
		white-space: pre;
	}

	.prose :global(h3) {
		margin-top: var(--space-6);
		margin-bottom: var(--space-3);
	}

	.prose :global(p) {
		margin-bottom: var(--space-4);
	}

	.prose :global(a) {
		color: var(--color-primary);
	}
</style>
