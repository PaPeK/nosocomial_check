import {readFile} from "node:fs/promises";

const source = new URL("../../../data/pone_review_S1_table.csv", import.meta.url);
process.stdout.write(await readFile(source, "utf8"));
