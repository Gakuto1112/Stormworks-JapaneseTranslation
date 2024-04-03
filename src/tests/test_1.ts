/**
 * **** テスト1 ****
 * 日本語の文章の中に禁止文字が含まれていないか確認する。
 * 禁止文字は読点、句読点、全角空白
 */

import { readConfig } from "../utils/config_reader";
import { streamTranslationData } from "../utils/data_reader";
import { warn, error } from "../utils/logger";

async function test1(): Promise<void> {
    console.info("Checking prohibited characters...");
    
    const prohibitedCharacters: string[] = (await readConfig()).prohibited_characters;
    const regex: RegExp = new RegExp(`[${prohibitedCharacters.join("")}]`);
    let errorFound: boolean = false;
    
    await streamTranslationData((line: number, id: string, en?: string, local?: string) => {
        if(local != undefined) {
            if(regex.test(local)) {
                error(line, `A prohibited character detected at line ${line}.`);
                errorFound = true;
            }
        }
        else warn(line, "Cannot find local string.");
    });
    
    if(errorFound) {
        console.error(`Detected one or more Prohibited characters! You cannot use these characters: ["${prohibitedCharacters.join("\", \"")}"]. Please remove them. For punctuation marks, please replace them with commas and periods.`);
        process.exit(1);
    }
    else {
        console.info("Finished checking prohibited characters. No prohibited character detected.");
        process.exit(0);
    }
}

test1();