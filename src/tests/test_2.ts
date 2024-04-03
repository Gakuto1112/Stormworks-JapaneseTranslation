/**
 * **** テスト2 ****
 * 日本語訳の追加し忘れをチェックする。
 * 英語も空白の場合は日本語が空白でも無視する。
 */

import { streamTranslationData } from "../utils/data_reader";
import { error } from "../utils/logger";

async function test2(): Promise<void> {
    console.info("Checking local strings...");
    
    let errorFound: boolean = false;
    
    await streamTranslationData((line: number, id: string, en?: string, local?: string) => {
        if(en != undefined) {
            if(en.length > 0 && (local == undefined || local.length == 0)) {
                error(line, `Cannot find local string at line ${line}.`);
                errorFound = true;
            }
        }
    });
    
    if(errorFound) {
        console.error("One or more lines are missing their local strings! Please add local strings.");
        process.exit(1);
    }
    else {
        console.info("Finished checking local strings. No missing line detected.");
        process.exit(0);
    }
}

test2();