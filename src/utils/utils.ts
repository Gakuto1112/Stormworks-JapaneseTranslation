import fs from "fs";
import readline from "readline";

/**
 * 翻訳データをストリーム処理する。
 * @param callback 翻訳キー毎に呼ばれるコールバック関数
 */
export async function streamTranslationData(callback: (id: string, en?: string, local?: string) => void): Promise<void> {
    return new Promise((resolve: () => void) => {
        const reader: readline.Interface = readline.createInterface(fs.createReadStream("../translation_data/japanese.tsv", {encoding: "utf-8"}));
        reader.addListener("line", (line: string) => {
            const lineSplit: string[] = line.split("\t");
            callback(lineSplit[0], lineSplit[2], lineSplit[3]);
        });
        reader.addListener("close", () => resolve());
    });
}