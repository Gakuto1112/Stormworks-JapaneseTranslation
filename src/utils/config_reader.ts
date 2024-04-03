import fs from "fs";

/**
 * 設定ファイルのデータ構造
 */
export interface Config {
    prohibited_characters: string[]
}

/**
 * 設定ファイルから設定を読み込む
 * @returns 読み込んだ設定のオブジェクト
 */
export async function readConfig(): Promise<Config> {
    const configData: Config = JSON.parse(fs.readFileSync("../config.json", {encoding: "utf-8"})) as Config;
    console.info("Loaded config data.");
    return configData;
}