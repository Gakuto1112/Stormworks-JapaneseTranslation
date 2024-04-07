import fs from "fs";
import readline from "readline";
import { ReasonCode, TestPoint, TestResult } from "../utils/test_result";

/**
 * Botレビューのオプションデータ
 */
interface ReviewOptions {
    /** レビューを行う対象のコミットID */
    commit_id: string,
    
    /** レビューコメント */
    body: string,
    
    /** レビューの種類 */
    event: "APPROVE" | "COMMENT" | "REQUEST_CHANGES",
    
    /** 行内コメントの配列 */
    comments: LineComment[]
}

/**
 * 行内コメントのデータ構造
 */
interface LineComment {
    /** コメントを行う対象のファイル名 */
    path: string,
    
    /**
     * コメントを行う対象の行番号
     * 行番号は`git diff`を行った際の差分表示の各ハンク始めの"@@"の次の行を1行目とした際の行番号を入力する。
     */
    position: number,
    
    /** レビューコメント */
    body: string
}

/**
 * Botレビュー用のデータを出力する。
 * @param commitId レビュー対象のコミットID
 * @param test1ResultJson テスト1の結果を示すJSON形式の文字列
 * @param test2ResultJson テスト2の結果を示すJSON形式の文字列
 */
async function createReviewData(commitId: string, test1ResultJson: string, test2ResultJson: string): Promise<void> {
    return new Promise(async (resolve: () => void) => {
        const reviewOptions: ReviewOptions = {
            commit_id: commitId,
            body: "## Test Results\n### Check prohibited characters\nThis test checks whether you use prohibited characters or not in your changes.\n\n**Result: ",
            event: "COMMENT",
            comments: []
        };
        
        const testResults: TestResult[] = [JSON.parse(test1ResultJson), JSON.parse(test2ResultJson)];
        //レビュー判定とコメントを作成
        reviewOptions.event = testResults[0].passed && testResults[1].passed ? "COMMENT" : "REQUEST_CHANGES";
        if(testResults[0].passed) reviewOptions.body += "🟢 Passed**\n\nNo prohibited character detected in your changes.\n\n";
        else {
            reviewOptions.body += "🔴 Failed**\n\nOne or more prohibited characters detected in your changes. Lines that include prohibited characters are followings:\n";
            reviewOptions.body += testResults[0].points.map((point: TestPoint) => `- Line ${point.line}\n`).join("");
            reviewOptions.body += "\nPlease remove or replace them.\n\n";
        }
        reviewOptions.body += "### Check missing translations\nThis test checks whether there are one or more missing translations or not in your changes.\n\n**Result: ";
        if(testResults[1].passed) reviewOptions.body += "🟢 Passed**\n\nNo missing translation detected in your changes.\n\n";
        else {
            reviewOptions.body += "🔴 Failed**\n\nOne or more missing translations detected in your changes. Lines whose translation is missing are followings:\n";
            reviewOptions.body += testResults[1].points.map((point: TestPoint) => `- Line ${point.line}\n`).join("");
            reviewOptions.body += "\nPlease fill all translations\n\n";
        }
        reviewOptions.body += "For more information about tests, please see [CONTRIBUTING.md](https://github.com/Gakuto1112/Stormworks-JapaneseTranslation/blob/main/.github/CONTRIBUTING.md#翻訳のルールについて).";
        
        //ソースファイルへのレビューコメントを作成
        if(reviewOptions.event == "REQUEST_CHANGES") {
            async function generateLineComments(): Promise<void> {
                return new Promise((innerResolve: () => void) => {
                    const reader: readline.Interface = readline.createInterface(fs.createReadStream("../../out/diff.log", {encoding: "utf-8"}));
                    let isTargetFile: boolean = false;
                    let isFirstHunk: boolean = false;
                    let lineCounter: number = 1;
                    let fileLineCounter: number = 1;
                    reader.addListener("line", (line: string) => {
                        if(/^diff --git a\/src\/translation_data\/japanese\.tsv b\/src\/translation_data\/japanese\.tsv$/.test(line)) {
                            isTargetFile = true;
                            isFirstHunk = true;
                        }
                        else if(line.startsWith("diff --git a/")) isTargetFile = false;
                        else if(/^@@\s-\d+,\d+\s\+\d+,\d+\s@@/.test(line) && isTargetFile) {
                            if(isFirstHunk) {
                                lineCounter = 1;
                                isFirstHunk = false;
                            }
                            const hunkData: RegExpMatchArray = line.match(/^@@\s-(\d+),(\d+)\s\+(\d+),(\d+)\s@@/) as RegExpMatchArray;
                            fileLineCounter = Number(hunkData[3]);
                        }
                        else if(isTargetFile && !isFirstHunk) {
                            if(line.startsWith(" ") || line.startsWith("+")) {
                                let linePoints: TestPoint[] = [];
                                testResults.forEach((result: TestResult) => linePoints = linePoints.concat(result.points.filter((point: TestPoint) => point.line == fileLineCounter)));
                                if(linePoints.length > 0) {
                                    reviewOptions.comments.push({
                                        path: "src/translation_data/japanese.tsv",
                                        position: lineCounter,
                                        body: linePoints.map((point: TestPoint) => point.reason == ReasonCode.USED_PROHIBITED_CHARS ? "Used one or more prohibited characters in this line." : "A translation is missing in this line.").join("\n\n")
                                    });
                                }
                                fileLineCounter++;
                            }
                            lineCounter++;
                        }
                    });
                    reader.addListener("close", () => innerResolve());
                });
            }
            
            await generateLineComments();
        }
        
        //レビューデータを出力
        fs.writeFileSync("../../out/review.json", JSON.stringify(reviewOptions), {encoding: "utf-8"});
        
        resolve();
    });
}

createReviewData(process.argv[2], process.argv[3], process.argv[4]);