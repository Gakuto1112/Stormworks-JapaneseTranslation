import fs from "fs";
import { streamTranslationData } from "../utils/data_reader";
import { TestResult } from "../utils/test_result";

/**
 * テストを行う機能を提供する抽象クラス
 */
export abstract class TestBase {
    /**
     * テスト結果
     */
    protected readonly testResult: TestResult = {
        passed: true,
        points: []
    }
    
    /**
     * テスト実行時に各翻訳キーに対して実行する関数
     * @param line 翻訳ファイルの行番号
     * @param id コンポーネントID。コンポーネントに関する翻訳キー以外は空文字になる。
     * @param en 英語原文。翻訳ファイルが不完全だとundefinedになっていることもある。
     * @param local 日本訳文。翻訳ファイルが不完全だとundefinedになっていることもある。
     */
    protected abstract testFunction(line: number, id: string, en?: string, local?: string): void;
    
    /**
     * テスト結果を初期化する。
     */
    private initializeTestResult(): void {
        this.testResult.passed = true;
        this.testResult.points = [];
    }
    
    /**
     * テストを実行する。
     * @returns テストに合格したかどうか
     */
    public async run(): Promise<boolean> {
        this.initializeTestResult();
        await streamTranslationData("../translation_data/japanese.tsv", (line: number, id: string, en?: string, local?: string) => this.testFunction(line, id, en, local));
        return this.testResult.passed;
    }
    
    /**
     * テスト結果をファイルに書き出す。
     */
    public exportTestResult() {
        fs.writeFileSync("../../out/result.json", JSON.stringify(this.testResult), {encoding: "utf-8"});
    }
}