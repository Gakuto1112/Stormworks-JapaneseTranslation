import fs from "fs";
import readline from "readline";

/**
 * 翻訳データをストリーム処理する。
 * @param path 翻訳データまでのパス
 * @param callback 翻訳キー毎に呼ばれるコールバック関数
 */
export async function streamTranslationData(path: string, callback: (line: number, id: string, en?: string, local?: string) => void): Promise<void> {
    return new Promise((resolve: () => void) => {
        let lineNum: number = 1;
        const reader: readline.Interface = readline.createInterface(fs.createReadStream(path, {encoding: "utf-8"}));
        reader.addListener("line", (line: string) => {
            const lineSplit: string[] = line.split("\t");
            callback(lineNum++, lineSplit[0], lineSplit[2], lineSplit.length > 3 ? lineSplit.slice(3).join("\t"): undefined);
        });
        reader.addListener("close", () => resolve());
    });
}
