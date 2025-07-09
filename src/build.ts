import fs from "fs";
import { streamTranslationData } from "./utils/data_reader";
import { warn } from "console";
import { readConfig } from "./utils/config_reader";

/**
 * 翻訳データをビルドする。
 */
async function build(): Promise<void> {
    console.info("Building translation data...");
    
    const writeStream: fs.WriteStream = fs.createWriteStream("../out/japanese.tsv", {encoding: "utf-8"});
    const separator: string = (await readConfig("./config.json")).build.separator;
    
    await streamTranslationData("./translation_data/japanese.tsv", (line: number, id: string, en?: string, local?: string) => {
        if(en != undefined) {
            if(local != undefined) {
                if(/^def_.+_name$/.test(id)) writeStream.write(`${id}\t\t${en}\t${local}${separator}${en}\n`);
                else writeStream.write(`${id}\t\t${en}\t${local}\n`);
            }
            else {
                warn(line, `Cannot find local string at line ${line}.`);
                writeStream.write(`${id}\t\t${en}\n`);
            }
        }
        else if(id.length > 0) writeStream.write(`${id}\n`);
        
    });
    writeStream.close();
    
    console.info("Finished building translation data.");
}

build();
