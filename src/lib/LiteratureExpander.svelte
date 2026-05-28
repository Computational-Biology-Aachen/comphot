<script lang="ts">
  import * as m from "$lib/paraglide/messages";
  import {
    Accordion as Expander,
    Li,
    Link,
    Text,
    Ul,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";
</script>

<Expander title={m.literature()}>
  <Text>{@html marked.parseInline(m.literature_onpage())}</Text>
  <Ul>
    <Li>
      Matuszyńska, A., Heidari, S., Jahns, P., &amp; Ebenhöh, O. (2016). A
      mathematical model of non-photochemical quenching to study short-term
      light memory in plants.
      <em>Biochimica et Biophysica Acta (BBA) - Bioenergetics</em>, 1857(12),
      1860-1869.
      <Link href="https://doi.org/10.1016/j.bbabio.2016.09.003"
        >https://doi.org/10.1016/j.bbabio.2016.09.003</Link
      >
    </Li>
  </Ul>
</Expander>
