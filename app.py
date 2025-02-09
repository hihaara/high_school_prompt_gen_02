import streamlit as st
import streamlit.components.v1 as components
from datetime import date

# ページ設定（タイトル、ワイドレイアウト）
st.set_page_config(page_title="ChatGPTプロンプト生成ツール", layout="wide")

# ページタイトルと説明
st.title("ChatGPT プロンプト生成ツール")
st.markdown("""
このツールは、日本の高等学校の教員向けに、ChatGPTへ送信するプロンプトを簡単に生成するためのWebアプリです。
※ 個人情報は一切入力しないようご注意ください。
※ 「個人情報入力禁止の同意」にチェックを入れると、各種入力項目が表示されます。
※ できるだけクリック操作のみで入力できるよう工夫しています。
""")

# ===============================
# サイドバー（右側）：使い方・注意事項
# ===============================
st.sidebar.header("使い方・注意事項")
st.sidebar.markdown("""
1. **個人情報の入力禁止に同意**
　個人情報は入力しないでください。同意すると、具体的なプロンプト項目が表示されます。
2. **業務内容の選択**
　各質問はクリックや選択操作のみで入力できるようになっています。
3. **プロンプトの確認とコピー**
　入力内容をもとに生成されたプロンプトがサイドバーに表示されます。
　「コピーする」ボタンで内容をクリップボードにコピーし、[ChatGPT](https://chat.openai.com) に貼り付けてご利用ください。
""")
st.sidebar.info("※ 個人情報の入力は行わないでください。")

# ===============================
# メイン画面（左側）
# ===============================
st.header("ユーザー入力（メイン画面）")

# 【質問１】個人情報の入力禁止の確認（チェックボックス）
agree = st.checkbox("【必須】個人情報を入力しないことに同意しますか？")
if not agree:
    st.warning("※ 個人情報の入力は禁止されています。同意いただくまで、次の入力項目は表示されません。")
    prompt_text = ""
else:
    # 【質問２】どのようなプロンプトを作成しますか？
    st.subheader("どのようなプロンプトを作成しますか？")
    prompt_options = [
        "小テストの作成",
        "メール文面の作成",
        "学習指導案の原案作成",
        "学級通信の作成",
        "保護者連絡文面の作成",
        "リマインドの作成",
        "業務の分割"
    ]
    prompt_type = st.selectbox("業務内容を選択してください", options=prompt_options)

    # 各種追加質問の回答を格納する辞書
    additional_info = {}

    if prompt_type == "小テストの作成":
        st.markdown("#### 小テストの作成に必要な情報")
        # 対象教科の選択：数学、英語、国語、理科（細分化）、社会（細分化）、その他
        subject_category = st.radio("大分類を選択してください", options=["数学", "英語", "国語", "理科", "社会", "その他"])
        if subject_category == "理科":
            subject_detail = st.radio("理科の科目を選択してください", options=["化学", "生物", "物理", "地学"])
            additional_info["対象教科"] = f"理科（{subject_detail}）"
        elif subject_category == "社会":
            subject_detail = st.radio("社会の科目を選択してください", options=["地理", "日本史", "世界史", "倫理", "政治経済"])
            additional_info["対象教科"] = f"社会（{subject_detail}）"
        else:
            additional_info["対象教科"] = subject_category

        # 難易度：5段階の選択
        difficulty_options = [
            "1. 非常に易しい（高校入学時レベル）",
            "2. 易しい（基礎理解レベル）",
            "3. 普通（標準的難易度）",
            "4. やや難しい（応用力を問うレベル）",
            "5. 非常に難しい（国立大学入試問題レベル）"
        ]
        additional_info["難易度"] = st.radio("テストの難易度は？", options=difficulty_options)
        # 問題数：1, 3, 5, 10の4択
        additional_info["問題数"] = st.radio("問題数は？", options=[1, 3, 5, 10])
        # 補足情報
        additional_info["補足情報"] = st.text_area("追加の補足情報（任意）", placeholder="例：出題傾向、使用する時間など")

    elif prompt_type == "メール文面の作成":
        st.markdown("#### メール文面作成に必要な情報")
        additional_info["メールの目的"] = st.radio("メールの目的は？", options=["連絡", "依頼", "報告", "お礼", "その他"])
        additional_info["宛先"] = st.radio("宛先は？", options=["保護者", "同僚", "上司", "生徒", "その他"])
        additional_info["要望・依頼内容"] = st.radio("伝えたい内容は？", options=["資料提出依頼", "会議設定", "スケジュール調整", "その他"])
        # 追加項目：送信希望日時
        additional_info["送信希望日時"] = st.selectbox("送信希望日時は？", options=["すぐに", "今日中", "明日以降"])
        additional_info["補足情報"] = st.text_area("追加の補足情報（任意）", placeholder="例：本文のトーン、署名など")

    elif prompt_type == "学習指導案の原案作成":
        st.markdown("#### 学習指導案作成に必要な情報")
        additional_info["授業形式"] = st.radio("授業の形式は？", options=["講義形式", "グループワーク", "実習", "ディスカッション", "その他"])
        additional_info["重点事項"] = st.radio("重点事項は？", options=["基礎理解", "応用力", "実践力", "創造力", "その他"])
        additional_info["対象学年"] = st.radio("対象の高校学年は？", options=["高校1年生", "高校2年生", "高校3年生"])
        # 対象クラスの選択肢を「1組」「2組」「3組」に変更
        additional_info["対象クラス"] = st.radio("対象クラスは？", options=["1組", "2組", "3組", "4組","5組"])
        # 使用教材：複数選択可能
        additional_info["使用教材"] = st.multiselect("使用する教材を選択（複数選択可）",
                                                     options=["教科書", "プリント", "映像教材", "オンライン資料", "その他"])
        additional_info["補足情報"] = st.text_area("追加の補足情報（任意）", placeholder="例：生徒の習熟度に合わせた工夫など")

    elif prompt_type == "学級通信の作成":
        st.markdown("#### 学級通信作成に必要な情報")
        additional_info["連絡内容"] = st.radio("連絡内容は？", options=["今月の行事", "学校行事", "休校情報", "その他"])
        additional_info["お知らせ内容"] = st.radio("お知らせ内容は？", options=["試験情報", "イベント情報", "クラブ活動", "その他"])
        additional_info["その他伝えたい事項"] = st.radio("その他伝えたい事項は？", options=["特になし", "追記あり"])
        # 追加項目：通信発行の頻度
        additional_info["発行頻度"] = st.selectbox("発行頻度は？", options=["月1回", "月2回", "不定期"])
        additional_info["補足情報"] = st.text_area("追加の補足情報（任意）", placeholder="例：文体やレイアウトの希望など")

    elif prompt_type == "保護者連絡文面の作成":
        st.markdown("#### 保護者連絡文面作成に必要な情報")
        additional_info["連絡の目的"] = st.radio("連絡の目的は？", options=["行事案内", "連絡事項", "個別連絡", "その他"])
        additional_info["伝えたい内容"] = st.radio("伝えたい内容は？", options=["詳細な案内", "簡潔な連絡", "注意喚起", "その他"])
        additional_info["締めのメッセージ"] = st.radio("締めの一言は？", options=["よろしくお願いします", "ご確認ください", "ご対応の程お願い申し上げます", "その他"])
        # 追加項目：保護者へのフォローアップ方法
        additional_info["フォローアップ方法"] = st.radio("フォローアップ方法は？", options=["電話", "メール", "面談", "その他"])
        additional_info["補足情報"] = st.text_area("追加の補足情報（任意）", placeholder="例：連絡の背景、緊急度など")

    elif prompt_type == "リマインドの作成":
        st.markdown("#### リマインド作成に必要な情報")
        additional_info["リマインド内容"] = st.radio("リマインドする内容は？", options=["提出期限のリマインド", "会議のリマインド", "イベントのリマインド", "その他"])
        additional_info["実施日"] = st.date_input("実施日を選択してください", value=date.today()).strftime("%Y-%m-%d")
        additional_info["時間帯"] = st.radio("実施時間帯は？", options=["午前", "午後", "夕方"])
        additional_info["対象者"] = st.radio("対象者は？", options=["全員", "特定のクラス", "特定のグループ", "その他"])
        # 追加項目：リマインドの頻度
        additional_info["リマインド頻度"] = st.selectbox("リマインド頻度は？", options=["1回", "複数回", "状況に応じて"])
        additional_info["補足情報"] = st.text_area("追加の補足情報（任意）", placeholder="例：リマインドの注意点など")

    elif prompt_type == "業務の分割":
        st.markdown("#### 業務分割に必要な情報")
        additional_info["業務内容"] = st.radio("業務内容は？", options=["授業準備", "試験作成", "部活動運営", "書類作成", "その他"])
        additional_info["担当者数"] = st.selectbox("担当者数は？", options=list(range(1, 11)))
        additional_info["期間"] = st.radio("業務の期間は？", options=["本日中", "今週中", "来週まで", "今月中"])
        additional_info["分割の希望"] = st.radio("分割の希望は？", options=["役割分担", "作業の順序指定", "担当者ごとの分担", "その他"])
        # 追加項目：作業分担の優先順位
        additional_info["優先順位"] = st.selectbox("作業の優先順位は？", options=["高", "中", "低"])
        additional_info["補足情報"] = st.text_area("追加の補足情報（任意）", placeholder="例：各担当者の得意分野など")

    # 入力された情報からプロンプト文を生成
    # 小テストの場合はWordに貼り付けることを想定した書式にする
    if prompt_type == "小テストの作成":
        prompt_text = "【Word用フォーマット】\n"
        prompt_text += "■ 小テスト作成\n"
        prompt_text += f"【対象教科】： {additional_info.get('対象教科')}\n"
        prompt_text += f"【難易度】： {additional_info.get('難易度')}\n"
        prompt_text += f"【問題数】： {additional_info.get('問題数')} 問\n"
        prompt_text += f"【補足情報】： {additional_info.get('補足情報')}\n"
        prompt_text += "\n【以下の条件に従い、小テストの問題とその解答を作成してください】\n"
        prompt_text += "・問題は番号順に列挙し、その後に対応する解答を同じ番号で出力すること。\n"
        prompt_text += "・問題文と解答はWordに貼り付けた際に見やすい書式とすること。\n"
        prompt_text += "\n【問題】\n"
        prompt_text += "(ここに問題文を出力してください。)\n"
        prompt_text += "\n【解答】\n"
        prompt_text += "(ここに各問題の解答を出力してください。)\n"
    else:
        prompt_text = f"ChatGPTに送信するプロンプト:\n- 業務内容: {prompt_type}\n"
        if additional_info:
            for key, value in additional_info.items():
                prompt_text += f"- {key}: {value}\n"

    st.success("プロンプトが生成されました。サイドバーをご確認ください。")

# ===============================
# サイドバー（右側）：生成されたプロンプトの表示とコピー機能
# ===============================
if agree and prompt_text:
    st.sidebar.header("生成されたプロンプト")
    st.sidebar.text_area("プロンプト（コピーしてChatGPTへ貼り付け）", value=prompt_text, height=300, key="prompt_box")

    # コピー用ボタンとChatGPTリンクを横並びに表示するためHTMLを利用
    copy_button_html = """
    <div style="display:flex; align-items:center; gap:10px; margin-top:10px;">
      <button id="copy-btn" style="padding:5px 10px;">コピーする</button>
      <a href="https://chat.openai.com" target="_blank" style="font-size:16px; text-decoration: none;">ChatGPTを開く</a>
    </div>
    <script>
    document.getElementById("copy-btn").addEventListener("click", function(){
      var ta = window.parent.document.querySelector('textarea[aria-label="プロンプト（コピーしてChatGPTへ貼り付け）"]');
      if(ta){
        navigator.clipboard.writeText(ta.value).then(function() {
          alert("クリップボードにコピーしました！");
        }, function(err) {
          alert("コピーに失敗しました。");
        });
      } else {
        alert("テキストエリアが見つかりません。");
      }
    });
    </script>
    """
    components.html(copy_button_html, height=100)
else:
    st.sidebar.info("※ 個人情報入力禁止に同意すると、プロンプトが生成されます。")
