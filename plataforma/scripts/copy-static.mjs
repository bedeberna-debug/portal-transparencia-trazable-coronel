import { cpSync, existsSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

const plataforma = resolve(fileURLToPath(new URL("..", import.meta.url)));
const dist = resolve(plataforma, "dist");

for (const directorio of ["data", "fuentes", "docs"]) {
  const origen = resolve(plataforma, directorio);
  if (!existsSync(origen)) {
    throw new Error(`Falta el directorio estático requerido: ${origen}`);
  }
  cpSync(origen, resolve(dist, directorio), { recursive: true });
}

writeFileSync(resolve(dist, ".nojekyll"), "", "utf8");
console.log("Datos, fuentes y documentos copiados a dist/; .nojekyll creado.");
