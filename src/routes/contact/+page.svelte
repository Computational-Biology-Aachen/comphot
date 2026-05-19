<script lang="ts">
  import { base } from "$app/paths";
  import * as m from "$lib/paraglide/messages";
  import {
    Button,
    H1,
    H2,
    InputChoice,
    Main,
    PageNav,
    Pre,
    Section,
    Text,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";

  const bibTexContent = `@article{
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

  let selectedFormat = $state<"BibTeX" | "RIS" | "EndNote">("BibTeX");

  function getCiteContent() {
    if (selectedFormat === "BibTeX") return bibTexContent;
    if (selectedFormat === "RIS") return risContent;
    if (selectedFormat === "EndNote") return endnoteContent;
    return "";
  }

  function getDownloadFilename() {
    if (selectedFormat === "BibTeX") return "ComPhot.bib";
    if (selectedFormat === "RIS") return "ComPhot.ris";
    if (selectedFormat === "EndNote") return "ComPhot.enw";
    return "";
  }

  function downloadCite() {
    const content = getCiteContent();
    const filename = getDownloadFilename();
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }
</script>

<svelte:head>
  <title>{m.cont_header()} | ComPhot</title>
</svelte:head>

<Main width="narrow">
  <H1>
    <span aria-hidden="true">📬 </span>
    {m.cont_header()}
  </H1>

  <PageNav
    base={base}
    prev={{ href: "/conclusion", label: m.sde_pagenames_conclusion() }}
  />

  <Text>
    {m.cont_subheader()}
  </Text>

  <Section>
    <h3>Sarah Philipps</h3>
    <ul>
      <li>
        <strong>{m.cont_email()}</strong>
        <a href="mailto:sarah.philipps@rwth-aachen.de"
          >sarah.philipps@rwth-aachen.de</a
        >
      </li>
      <li><strong>{m.cont_topics()}</strong> {m.cont_topics_sarah()}</li>
    </ul>

    <h3>Tobias Pfennig</h3>
    <ul>
      <li>
        <strong>{m.cont_email()}</strong>
        <a href="mailto:tobias.pfennig@rwth-aachen.de"
          >tobias.pfennig@rwth-aachen.de</a
        >
      </li>
      <li><strong>{m.cont_topics()}</strong> {m.cont_topics_tobias()}</li>
      <li>
        <strong>{m.cont_website()}</strong>
        <a
          href="https://www.cpbl.rwth-aachen.de/cms/CPBL/Die-Juniorprofessur/Unser/~wljpm/Tobias-Pfennig/"
          target="_blank"
          rel="noopener">RWTH Aachen</a
        >
      </li>
    </ul>

    <h3>Elouen Corvest</h3>
    <ul>
      <li>
        <strong>{m.cont_email()}</strong>
        <a href="mailto:elouen.corvest@rwth-aachen.de"
          >elouen.corvest@rwth-aachen.de</a
        >
      </li>
      <li><strong>{m.cont_topics()}</strong> {m.cont_topics_elouen()}</li>
      <li>
        <strong>{m.cont_website()}</strong>
        <a
          href="https://www.cpbl.rwth-aachen.de/cms/CPBL/Die-Juniorprofessur/Unser/~wljuk/Elouen-Corvest/lidx/1/"
          target="_blank"
          rel="noopener">RWTH Aachen</a
        >
      </li>
    </ul>

    <h3>Marvin van Aalst</h3>
    <ul>
      <li>
        <strong>{m.cont_email()}</strong>
        <a href="mailto:marvin.van.aalst@hhu.de">marvin.van.aalst@hhu.de</a>
      </li>
      <li><strong>{m.cont_topics()}</strong> {m.cont_topics_marvin()}</li>
      <li>
        <strong>{m.cont_website()}</strong>
        <a
          href="https://www.qtb.hhu.de/"
          target="_blank"
          rel="noopener">Heinrich Heine University Duesseldorf</a
        >
      </li>
    </ul>

    <h3>Lisa Fürtauer</h3>
    <ul>
      <li>
        <strong>{m.cont_email()}</strong>
        <a href="mailto:lisa.fuertauer@bio3.rwth-aachen.de"
          >lisa.fuertauer@bio3.rwth-aachen.de</a
        >
      </li>
      <li><strong>{m.cont_topics()}</strong> {m.cont_topics_lisa()}</li>
      <li>
        <strong>{m.cont_website()}</strong>
        <a
          href="https://www.bio3.rwth-aachen.de/cms/BIO3/Das-Institut/~tcejj/Juniorprofessur-Molekulare-Systembiologi/"
          target="_blank"
          rel="noopener">RWTH Aachen</a
        >
      </li>
    </ul>

    <h3>Anna Matuszyńska</h3>
    <ul>
      <li>
        <strong>{m.cont_email()}</strong>
        <a href="mailto:anna.matuszynska@rwth-aachen.de"
          >anna.matuszynska@rwth-aachen.de</a
        >
      </li>
      <li><strong>{m.cont_topics()}</strong> {m.cont_topics_anna()}</li>
      <li>
        <strong>{m.cont_website()}</strong>
        <a
          href="https://www.cpbl.rwth-aachen.de/cms/CPBL/Die-Juniorprofessur/Unser/~ywkwc/Anna-Matuszy-324-ska/"
          target="_blank"
          rel="noopener">RWTH Aachen</a
        >
      </li>
    </ul>
  </Section>

  <Text>
    {m.cont_hours()}
  </Text>
  <Text>
    {m.cont_thanks()}
  </Text>

  <!-- Section: citation -->
  <H2>{m.cont_cite()}</H2>
  <Text>
    Computational Photosynthesis (ComPhot): Simulation-Based Learning Platform
    to Study Photosynthesis, The Plant Cell, 2024
  </Text>
  <InputChoice
    id="cite-format"
    label={m.cont_style()}
    bind:value={selectedFormat}
  >
    <option value="BibTeX">BibTeX</option>
    <option value="RIS">RIS</option>
    <option value="EndNote">EndNote</option>
  </InputChoice>
  <Pre>{getCiteContent()}</Pre>
  <Button onclick={downloadCite}>
    Download {getDownloadFilename()}
  </Button>

  <!-- Section: resources -->
  <H2>
    {@html marked.parseInline(m.cont_resources())}
  </H2>
  <Text>
    <!-- FIXME: break message into smaller pieces -->
    {@html marked.parse(m.programs_used())}
  </Text>

  <PageNav
    base={base}
    prev={{ href: "/conclusion", label: m.sde_pagenames_conclusion() }}
  />
</Main>
