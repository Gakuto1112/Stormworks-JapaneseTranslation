import fs from "fs";

/**
 * 設定ファイルのデータ構造
 */
export interface Config {
    build: {
        separator: string
    },
    test: {
        prohibited_characters: string[]
    }
}

/**
 * 設定ファイルから設定を読み込む
 * @param path 設定ファイルまでのパス
 * @returns 読み込んだ設定のオブジェクト
 */
export async function readConfig(path: string): Promise<Config> {
    const configData: Config = JSON.parse(fs.readFileSync(path, {encoding: "utf-8"})) as Config;
    console.info("Loaded config data.");
    return configData;
}