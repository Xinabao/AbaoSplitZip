"""
AbaoZip 国际化支持
支持 9 种语言：简体中文、繁體中文、英语、日语、韩语、德语、法语、西班牙语、葡萄牙语
"""

import locale

from core.version import APP_NAME, APP_VERSION, OFFICIAL_WEBSITE

LANGUAGES = {
    "简体中文": "zh",
    "繁體中文": "zh_TW",
    "English": "en",
    "日本語": "ja",
    "한국어": "ko",
    "Deutsch": "de",
    "Français": "fr",
    "Español": "es",
    "Português": "pt",
}

TEXTS = {
    "label_mode": {
        "zh": "打包模式:",
        "zh_TW": "打包模式:",
        "en": "Packing Mode:",
        "ja": "パッキングモード:",
        "ko": "포장 모드:",
        "de": "Packmodus:",
        "fr": "Mode d'emballage:",
        "es": "Modo de embalaje:",
        "pt": "Modo de embalagem:",
    },
    "mode_size": {
        "zh": "大小均衡 (最少分卷)",
        "zh_TW": "大小均衡 (最少分卷)",
        "en": "Size Balanced (Min Volumes)",
        "ja": "サイズバランス (最小巻数)",
        "ko": "크기 균형 (최소 볼륨)",
        "de": "Größenausgleich (Min. Volumen)",
        "fr": "Équilibre de taille (Vol. Min)",
        "es": "Equilibrio de tamaño (Vol. Mín)",
        "pt": "Equilíbrio de tamanho (Vol. Mín)",
    },
    "mode_dir": {
        "zh": "目录优先 (保持结构)",
        "zh_TW": "目錄優先 (保持結構)",
        "en": "Directory Priority (Keep Folder Structure)",
        "ja": "ディレクトリ優先 (構造保持)",
        "ko": "디렉터리 우선 (구조 유지)",
        "de": "Verzeichnispriorität (Struktur behalten)",
        "fr": "Priorité répertoire (Garder structure)",
        "es": "Prioridad directorio (Mantener estructura)",
        "pt": "Prioridade diretório (Manter estrutura)",
    },
    "label_exclude": {
        "zh": "排除文件:",
        "zh_TW": "排除檔案:",
        "en": "Exclude Files:",
        "ja": "除外ファイル:",
        "ko": "제외 파일:",
        "de": "Dateien ausschließen:",
        "fr": "Exclure fichiers:",
        "es": "Excluir archivos:",
        "pt": "Excluir arquivos:",
    },
    "hint_exclude": {
        "zh": "例如: *.git, *.tmp (逗号分隔)",
        "zh_TW": "例如: *.git, *.tmp (逗號分隔)",
        "en": "e.g. *.git, *.tmp (comma separated)",
        "ja": "例: *.git, *.tmp (カンマ区切り)",
        "ko": "예: *.git, *.tmp (쉼표 구분)",
        "de": "z.B. *.git, *.tmp (kommagetrennt)",
        "fr": "ex. *.git, *.tmp (séparé par virgule)",
        "es": "ej. *.git, *.tmp (separado por comas)",
        "pt": "ex. *.git, *.tmp (separado por vírgula)",
    },
    "btn_open_folder": {
        "zh": "打开输出文件夹",
        "zh_TW": "打開輸出資料夾",
        "en": "Open Output Folder",
        "ja": "出力フォルダを開く",
        "ko": "출력 폴더 열기",
        "de": "Ausgabeordner öffnen",
        "fr": "Ouvrir dossier sortie",
        "es": "Abrir carpeta salida",
        "pt": "Abrir pasta saída",
    },
    "app_title": {
        "zh": "AbaoZip — 分卷独立解压打包工具",
        "zh_TW": "AbaoZip — 分卷獨立解壓打包工具",
        "en": "AbaoZip — Volume Packer with Independent Extraction",
        "ja": "AbaoZip — 分割独立解凍パッカー",
        "ko": "AbaoZip — 분할 독립 압축 해제 도구",
        "de": "AbaoZip — Volumen-Packer mit unabhängiger Extraktion",
        "fr": "AbaoZip — Empaqueteur par volumes avec extraction indépendante",
        "es": "AbaoZip — Empaquetador por volúmenes con extracción independiente",
        "pt": "AbaoZip — Empacotador por volumes com extração independente",
    },
    "header_title": {
        "zh": "AbaoZip 分卷打包工具",
        "zh_TW": "AbaoZip 分卷打包工具",
        "en": "AbaoZip Volume Packer",
        "ja": "AbaoZip 分割パッカー",
        "ko": "AbaoZip 분할 압축 도구",
        "de": "AbaoZip Volumen-Packer",
        "fr": "AbaoZip Empaqueteur par volumes",
        "es": "AbaoZip Empaquetador por volúmenes",
        "pt": "AbaoZip Empacotador por volumes",
    },
    "header_desc": {
        "zh": "将大文件夹按指定大小分卷打包，每个分卷都是独立的 ZIP，可单独解压。",
        "zh_TW": "將大資料夾按指定大小分卷打包，每個分卷都是獨立的 ZIP，可單獨解壓。",
        "en": "Pack large folders into volume-sized ZIPs. Each volume is an independent ZIP that can be extracted separately.",
        "ja": "大きなフォルダを指定サイズで分割パック。各ボリュームは独立したZIPで個別に解凍可能。",
        "ko": "대용량 폴더를 지정 크기로 분할 압축. 각 볼륨은 독립적인 ZIP으로 개별 압축 해제 가능.",
        "de": "Große Ordner in Volumen-ZIPs packen. Jedes Volumen ist ein unabhängiges ZIP.",
        "fr": "Empaqueter de grands dossiers en ZIP par volumes. Chaque volume est un ZIP indépendant.",
        "es": "Empaquetar carpetas grandes en ZIPs por volúmenes. Cada volumen es un ZIP independiente.",
        "pt": "Empacotar pastas grandes em ZIPs por volumes. Cada volume é um ZIP independente.",
    },
    "header_bat_hint": {
        "zh": "打包完成后会同时生成「一键全部解压.bat」脚本，如需一次性解压所有分卷请运行该脚本。",
        "zh_TW": "打包完成後會同時產生「一鍵全部解壓.bat」腳本，如需一次性解壓所有分卷請執行該腳本。",
        "en": 'A "Extract All.bat" script will be generated after packing. Run it to extract all volumes at once.',
        "ja": "パック完了後「一括解凍.bat」スクリプトが生成されます。全ボリュームを一度に解凍するにはそれを実行してください。",
        "ko": '압축 완료 후 "전체 압축 해제.bat" 스크립트가 생성됩니다. 모든 볼륨을 한번에 해제하려면 실행하세요.',
        "de": 'Nach dem Packen wird ein "Alle entpacken.bat"-Skript erstellt. Führen Sie es aus, um alle Volumen zu entpacken.',
        "fr": 'Un script "Extraire tout.bat" sera généré après l\'empaquetage. Exécutez-le pour extraire tous les volumes.',
        "es": 'Se generará un script "Extraer todo.bat" después del empaquetado. Ejecútelo para extraer todos los volúmenes.',
        "pt": 'Um script "Extrair tudo.bat" será gerado após o empacotamento. Execute-o para extrair todos os volumes.',
    },
    "tab_pack": {
        "zh": "📦 打包",
        "zh_TW": "📦 打包",
        "en": "📦 Pack",
        "ja": "📦 パック",
        "ko": "📦 압축",
        "de": "📦 Packen",
        "fr": "📦 Empaqueter",
        "es": "📦 Empaquetar",
        "pt": "📦 Empacotar",
    },
    "tab_unpack": {
        "zh": "📂 解压",
        "zh_TW": "📂 解壓",
        "en": "📂 Extract",
        "ja": "📂 解凍",
        "ko": "📂 압축 해제",
        "de": "📂 Entpacken",
        "fr": "📂 Extraire",
        "es": "📂 Extraer",
        "pt": "📂 Extrair",
    },
    "tab_merge": {
        "zh": "🔗 合并解压",
        "zh_TW": "🔗 合併解壓",
        "en": "🔗 Merge & Extract",
        "ja": "🔗 結合解凍",
        "ko": "🔗 병합 및 추출",
        "de": "🔗 Zusammenführen",
        "fr": "🔗 Fusionner",
        "es": "🔗 Fusionar",
        "pt": "🔗 Mesclar",
    },
    "merge_desc": {
        "zh": "选择任意一个分卷 (.zip)，软件会自动查找同目录下的所有分卷并合并解压。",
        "zh_TW": "選擇任意一個分卷 (.zip)，軟體會自動尋找同目錄下的所有分卷並合併解壓。",
        "en": "Select any volume (.zip). The tool will automatically find and merge all related volumes in the same folder.",
        "ja": "任意のボリューム (.zip) を選択。同じフォルダ内の全ボリュームを自動検出し結合解凍します。",
        "ko": "임의의 볼륨 (.zip) 선택. 같은 폴더 내의 모든 볼륨을 자동으로 찾아 병합 해제합니다.",
        "de": "Wählen Sie ein beliebiges Volumen (.zip). Das Tool findet und extrahiert automatisch alle Teile.",
        "fr": "Sélectionnez n'importe quel volume (.zip). L'outil fusionnera tout le reste.",
        "es": "Seleccione cualquier volumen (.zip). La herramienta fusionará todo lo demás.",
        "pt": "Selecione qualquer volume (.zip). A ferramenta mesclará todo o resto.",
    },
    "label_select_part": {
        "zh": "选择分卷:",
        "zh_TW": "選擇分卷:",
        "en": "Select Part:",
        "ja": "ボリューム選択:",
        "ko": "볼륨 선택:",
        "de": "Volumen wählen:",
        "fr": "Choisir volume:",
        "es": "Elegir volumen:",
        "pt": "Escolher volume:",
    },
    "hint_select_part": {
        "zh": "选择任意一个分卷文件...",
        "zh_TW": "選擇任意一個分卷檔案...",
        "en": "Select any volume file...",
        "ja": "任意のボリュームファイルを選択...",
        "ko": "임의의 볼륨 파일 선택...",
        "de": "Beliebige Volumendatei auswählen...",
        "fr": "Sélectionnez un fichier volume...",
        "es": "Seleccione un archivo de volumen...",
        "pt": "Selecione um arquivo de volume...",
    },
    "btn_start_merge": {
        "zh": "开始合并解压",
        "zh_TW": "開始合併解壓",
        "en": "Start Merge & Extract",
        "ja": "結合解凍開始",
        "ko": "병합 해제 시작",
        "de": "Zusammenführen starten",
        "fr": "Lancer fusion",
        "es": "Iniciar fusión",
        "pt": "Iniciar mesclagem",
    },
    "btn_about": {
        "zh": "关于 / 帮助",
        "zh_TW": "關於 / 幫助",
        "en": "About / Help",
        "ja": "バージョン / ヘルプ",
        "ko": "정보 / 도움말",
        "de": "Über / Hilfe",
        "fr": "À propos / Aide",
        "es": "Acerca de / Ayuda",
        "pt": "Sobre / Ajuda",
    },
    "about_title": {
        "zh": "关于 AbaoZip",
        "zh_TW": "關於 AbaoZip",
        "en": "About AbaoZip",
        "ja": "AbaoZipについて",
        "ko": "AbaoZip 정보",
        "de": "Über AbaoZip",
        "fr": "À propos de AbaoZip",
        "es": "Acerca de AbaoZip",
        "pt": "Sobre o AbaoZip",
    },
    "about_content": {
        "zh": f"""<h3>{APP_NAME} v{APP_VERSION}</h3>
<p>一款支持独立解压的分卷打包工具。</p>
<p>🌐 <b>官方网站:</b> <a href="{OFFICIAL_WEBSITE}">{OFFICIAL_WEBSITE}</a></p>
<hr>
<b>使用帮助:</b>
<ul>
<li><b>打包:</b> 拖入文件夹，设置分卷大小，点击开始。</li>
<li><b>解压:</b> 拖入 ZIP 文件，点击解压。</li>
<li><b>合并:</b> 拖入任意分卷 (.zip)，自动合并解压所有关联分卷。</li>
</ul>
<p>开源协议: GPL v3</p>""",
        "zh_TW": f"""<h3>{APP_NAME} v{APP_VERSION}</h3>
<p>一款支援獨立解壓的分卷打包工具。</p>
<p>🌐 <b>官方網站:</b> <a href="{OFFICIAL_WEBSITE}">{OFFICIAL_WEBSITE}</a></p>
<hr>
<b>使用幫助:</b>
<ul>
<li><b>打包:</b> 拖入資料夾，設定分卷大小，點擊開始。</li>
<li><b>解壓:</b> 拖入 ZIP 檔案，點擊解壓。</li>
<li><b>合併:</b> 拖入任意分卷 (.zip)，自動合併解壓所有關聯分卷。</li>
</ul>
<p>開源協議: GPL v3</p>""",
        "en": f"""<h3>{APP_NAME} v{APP_VERSION}</h3>
<p>A volume packer with independent extraction support.</p>
<p>🌐 <b>Official Website:</b> <a href="{OFFICIAL_WEBSITE}">{OFFICIAL_WEBSITE}</a></p>
<hr>
<b>Quick Help:</b>
<ul>
<li><b>Pack:</b> Drag & drop folder, set volume size, click Start.</li>
<li><b>Extract:</b> Drag & drop ZIP file, click Extract.</li>
<li><b>Merge:</b> Drag any volume (.zip), it will auto-merge and extract all parts.</li>
</ul>
<p>License: GPL v3</p>""",
        "ja": f"""<h3>{APP_NAME} v{APP_VERSION}</h3>
<p>独立解凍をサポートする分割パッカー。</p>
<p>🌐 <b>公式サイト:</b> <a href="{OFFICIAL_WEBSITE}">{OFFICIAL_WEBSITE}</a></p>
<hr>
<b>ヘルプ:</b>
<ul>
<li><b>パック:</b> フォルダをドラッグ、サイズ設定、開始をクリック。</li>
<li><b>解凍:</b> ZIPをドラッグ、解凍をクリック。</li>
<li><b>結合:</b> 任意の分巻(.zip)をドラッグ、全パーツを自動結合解凍。</li>
</ul>
<p>ライセンス: GPL v3</p>""",
        "ko": f"""<h3>{APP_NAME} v{APP_VERSION}</h3>
<p>독립 압축 해제를 지원하는 분할 압축 도구입니다.</p>
<p>🌐 <b>공식 웹사이트:</b> <a href="{OFFICIAL_WEBSITE}">{OFFICIAL_WEBSITE}</a></p>
<hr>
<b>도움말:</b>
<ul>
<li><b>압축:</b> 폴더 드래그, 볼륨 크기 설정, 시작 클릭.</li>
<li><b>해제:</b> ZIP 파일 드래그, 해제 클릭.</li>
<li><b>병합:</b> 임의의 볼륨(.zip) 드래그, 전체 자동 병합 해제.</li>
</ul>
<p>라이선스: GPL v3</p>""",
        "de": f"""<h3>{APP_NAME} v{APP_VERSION}</h3>
<p>Ein Volumen-Packer mit unabhängiger Extraktion.</p>
<p>🌐 <b>Offizielle Website:</b> <a href="{OFFICIAL_WEBSITE}">{OFFICIAL_WEBSITE}</a></p>
<hr>
<b>Hilfe:</b>
<ul>
<li><b>Packen:</b> Ordner ziehen, Größe einstellen, Start klicken.</li>
<li><b>Entpacken:</b> ZIP ziehen, Entpacken klicken.</li>
<li><b>Zusammenführen:</b> Beliebiges Volumen (.zip) ziehen, alles automatisch zusammenführen.</li>
</ul>
<p>Lizenz: GPL v3</p>""",
        "fr": f"""<h3>{APP_NAME} v{APP_VERSION}</h3>
<p>Un empaqueteur de volumes avec extraction indépendante.</p>
<p>🌐 <b>Site officiel:</b> <a href="{OFFICIAL_WEBSITE}">{OFFICIAL_WEBSITE}</a></p>
<hr>
<b>Aide:</b>
<ul>
<li><b>Empaqueter:</b> Glisser le dossier, définir la taille, cliquer sur Démarrer.</li>
<li><b>Extraire:</b> Glisser le ZIP, cliquer sur Extraire.</li>
<li><b>Fusionner:</b> Glisser un volume (.zip), fusion automatique.</li>
</ul>
<p>Licence: GPL v3</p>""",
        "es": f"""<h3>{APP_NAME} v{APP_VERSION}</h3>
<p>Un empaquetador de volúmenes con extracción independiente.</p>
<p>🌐 <b>Sitio web oficial:</b> <a href="{OFFICIAL_WEBSITE}">{OFFICIAL_WEBSITE}</a></p>
<hr>
<b>Ayuda:</b>
<ul>
<li><b>Empaquetar:</b> Arrastrar carpeta, establecer tamaño, clic en Iniciar.</li>
<li><b>Extraer:</b> Arrastrar ZIP, clic en Extraer.</li>
<li><b>Fusionar:</b> Arrastrar volumen (.zip), fusión automática.</li>
</ul>
<p>Licencia: GPL v3</p>""",
        "pt": f"""<h3>{APP_NAME} v{APP_VERSION}</h3>
<p>Um empacotador de volumes com extração independente.</p>
<p>🌐 <b>Site oficial:</b> <a href="{OFFICIAL_WEBSITE}">{OFFICIAL_WEBSITE}</a></p>
<hr>
<b>Ajuda:</b>
<ul>
<li><b>Empacotar:</b> Arrastar pasta, definir tamanho, clicar em Iniciar.</li>
<li><b>Extrair:</b> Arrastar ZIP, clicar em Extrair.</li>
<li><b>Mesclar:</b> Arrastar volume (.zip), mesclagem automática.</li>
</ul>
<p>Licença: GPL v3</p>""",
    },
    "group_paths": {
        "zh": "路径设置",
        "zh_TW": "路徑設定",
        "en": "Path Settings",
        "ja": "パス設定",
        "ko": "경로 설정",
        "de": "Pfadeinstellungen",
        "fr": "Paramètres de chemin",
        "es": "Configuración de rutas",
        "pt": "Configuração de caminhos",
    },
    "label_source": {
        "zh": "源文件夹:",
        "zh_TW": "來源資料夾：",
        "en": "Source folder:",
        "ja": "ソースフォルダ:",
        "ko": "소스 폴더:",
        "de": "Quellordner:",
        "fr": "Dossier source :",
        "es": "Carpeta origen:",
        "pt": "Pasta origem:",
    },
    "hint_source": {
        "zh": "选择要打包的文件夹",
        "zh_TW": "選擇要打包的資料夾",
        "en": "Select the folder to pack",
        "ja": "パックするフォルダを選択",
        "ko": "압축할 폴더를 선택하세요",
        "de": "Wählen Sie den zu packenden Ordner",
        "fr": "Sélectionner le dossier à empaqueter",
        "es": "Seleccione la carpeta a empaquetar",
        "pt": "Selecione a pasta para empacotar",
    },
    "label_output": {
        "zh": "输出目录:",
        "zh_TW": "輸出目錄：",
        "en": "Output folder:",
        "ja": "出力先:",
        "ko": "출력 폴더:",
        "de": "Ausgabeordner:",
        "fr": "Dossier de sortie :",
        "es": "Carpeta de salida:",
        "pt": "Pasta de saída:",
    },
    "hint_output": {
        "zh": "选择分卷压缩包的保存位置",
        "zh_TW": "選擇分卷壓縮檔的儲存位置",
        "en": "Select where to save the volume ZIPs",
        "ja": "分割ZIPの保存先を選択",
        "ko": "분할 ZIP 저장 위치를 선택하세요",
        "de": "Wählen Sie den Speicherort für die Volumen-ZIPs",
        "fr": "Sélectionner où enregistrer les ZIP",
        "es": "Seleccione dónde guardar los ZIPs",
        "pt": "Selecione onde salvar os ZIPs",
    },
    "browse": {
        "zh": "浏览...",
        "zh_TW": "瀏覽...",
        "en": "Browse...",
        "ja": "参照...",
        "ko": "찾아보기...",
        "de": "Durchsuchen...",
        "fr": "Parcourir...",
        "es": "Examinar...",
        "pt": "Procurar...",
    },
    "group_settings": {
        "zh": "打包设置",
        "zh_TW": "打包設定",
        "en": "Pack Settings",
        "ja": "パック設定",
        "ko": "압축 설정",
        "de": "Pack-Einstellungen",
        "fr": "Paramètres d'empaquetage",
        "es": "Configuración de empaquetado",
        "pt": "Configurações de empacotamento",
    },
    "label_volume_size": {
        "zh": "分卷大小:",
        "zh_TW": "分卷大小：",
        "en": "Volume size:",
        "ja": "ボリュームサイズ:",
        "ko": "볼륨 크기:",
        "de": "Volumengröße:",
        "fr": "Taille du volume :",
        "es": "Tamaño del volumen:",
        "pt": "Tamanho do volume:",
    },
    "hint_volume_size": {
        "zh": "每卷的目标大小（实际会略有偏差以保证文件完整）",
        "zh_TW": "每卷的目標大小（實際會略有偏差以保證檔案完整）",
        "en": "Target size per volume (may vary slightly to keep files intact)",
        "ja": "各ボリュームの目標サイズ（ファイルの完全性を保つため多少変動します）",
        "ko": "볼륨당 목표 크기 (파일 무결성을 위해 약간의 차이가 있을 수 있음)",
        "de": "Zielgröße pro Volumen (kann leicht variieren)",
        "fr": "Taille cible par volume (peut varier légèrement)",
        "es": "Tamaño objetivo por volumen (puede variar ligeramente)",
        "pt": "Tamanho alvo por volume (pode variar ligeiramente)",
    },
    "label_compression": {
        "zh": "压缩级别:",
        "zh_TW": "壓縮級別：",
        "en": "Compression:",
        "ja": "圧縮レベル:",
        "ko": "압축 수준:",
        "de": "Komprimierung:",
        "fr": "Compression :",
        "es": "Compresión:",
        "pt": "Compressão:",
    },
    "group_password": {
        "zh": "密码与加密（可选）",
        "zh_TW": "密碼與加密（可選）",
        "en": "Password & Encryption (optional)",
        "ja": "パスワードと暗号化（任意）",
        "ko": "비밀번호 및 암호화 (선택)",
        "de": "Passwort & Verschlüsselung (optional)",
        "fr": "Mot de passe et chiffrement (optionnel)",
        "es": "Contraseña y cifrado (opcional)",
        "pt": "Senha e criptografia (opcional)",
    },
    "label_password": {
        "zh": "密码:",
        "zh_TW": "密碼：",
        "en": "Password:",
        "ja": "パスワード:",
        "ko": "비밀번호:",
        "de": "Passwort:",
        "fr": "Mot de passe :",
        "es": "Contraseña:",
        "pt": "Senha:",
    },
    "hint_password": {
        "zh": "留空则不加密",
        "zh_TW": "留空則不加密",
        "en": "Leave empty for no encryption",
        "ja": "空欄の場合は暗号化なし",
        "ko": "비워두면 암호화하지 않음",
        "de": "Leer lassen für keine Verschlüsselung",
        "fr": "Laisser vide pour ne pas chiffrer",
        "es": "Dejar vacío para no cifrar",
        "pt": "Deixe vazio para não criptografar",
    },
    "enc_zipcrypto": {
        "zh": "  ✅ Windows 10/11 资源管理器可直接解压，安全性一般",
        "zh_TW": "  ✅ Windows 10/11 檔案總管可直接解壓，安全性一般",
        "en": "  ✅ Windows 10/11 Explorer can extract directly, moderate security",
        "ja": "  ✅ Windows 10/11 エクスプローラーで直接解凍可能、セキュリティは普通",
        "ko": "  ✅ Windows 10/11 탐색기에서 직접 해제 가능, 보통 수준의 보안",
        "de": "  ✅ Windows 10/11 Explorer kann direkt entpacken, moderate Sicherheit",
        "fr": "  ✅ L'explorateur Windows 10/11 peut extraire directement, sécurité modérée",
        "es": "  ✅ El explorador de Windows 10/11 puede extraer directamente, seguridad moderada",
        "pt": "  ✅ O explorador do Windows 10/11 pode extrair diretamente, segurança moderada",
    },
    "enc_aes": {
        "zh": "  🔒 安全性高，需用 7-Zip / WinRAR 等工具解压",
        "zh_TW": "  🔒 安全性高，需用 7-Zip / WinRAR 等工具解壓",
        "en": "  🔒 High security, requires 7-Zip / WinRAR to extract",
        "ja": "  🔒 高セキュリティ、解凍には 7-Zip / WinRAR が必要",
        "ko": "  🔒 높은 보안, 압축 해제에 7-Zip / WinRAR 필요",
        "de": "  🔒 Hohe Sicherheit, erfordert 7-Zip / WinRAR zum Entpacken",
        "fr": "  🔒 Haute sécurité, nécessite 7-Zip / WinRAR pour extraire",
        "es": "  🔒 Alta seguridad, requiere 7-Zip / WinRAR para extraer",
        "pt": "  🔒 Alta segurança, requer 7-Zip / WinRAR para extrair",
    },
    "btn_start_pack": {
        "zh": "▶ 开始打包",
        "zh_TW": "▶ 開始打包",
        "en": "▶ Start Packing",
        "ja": "▶ パック開始",
        "ko": "▶ 압축 시작",
        "de": "▶ Packen starten",
        "fr": "▶ Démarrer l'empaquetage",
        "es": "▶ Iniciar empaquetado",
        "pt": "▶ Iniciar empacotamento",
    },
    "btn_cancel": {
        "zh": "取消",
        "zh_TW": "取消",
        "en": "Cancel",
        "ja": "キャンセル",
        "ko": "취소",
        "de": "Abbrechen",
        "fr": "Annuler",
        "es": "Cancelar",
        "pt": "Cancelar",
    },
    "unpack_desc": {
        "zh": "选择任意一个分卷文件（如 XXX_part001.zip），将自动识别并解压同组的所有分卷。\n也可以解压单个 ZIP / 7z / RAR 文件。",
        "zh_TW": "選擇任意一個分卷檔案（如 XXX_part001.zip），將自動識別並解壓同組的所有分卷。\n也可以解壓單個 ZIP / 7z / RAR 檔案。",
        "en": "Select any volume file (e.g. XXX_part001.zip) to automatically find and extract all volumes in the group.\nAlso supports single ZIP / 7z / RAR files.",
        "ja": "任意の分割ファイル（例: XXX_part001.zip）を選択すると、同グループの全ボリュームを自動検出して解凍します。\n単体の ZIP / 7z / RAR ファイルも解凍できます。",
        "ko": "분할 파일(예: XXX_part001.zip)을 선택하면 같은 그룹의 모든 볼륨을 자동으로 찾아 해제합니다.\n단일 ZIP / 7z / RAR 파일도 해제할 수 있습니다.",
        "de": "Wählen Sie eine beliebige Volumendatei (z.B. XXX_part001.zip), um alle Volumen der Gruppe automatisch zu finden und zu entpacken.\nUnterstützt auch einzelne ZIP / 7z / RAR Dateien.",
        "fr": "Sélectionnez n'importe quel fichier volume (ex: XXX_part001.zip) pour trouver et extraire automatiquement tous les volumes du groupe.\nSupporte aussi les fichiers ZIP / 7z / RAR individuels.",
        "es": "Seleccione cualquier archivo de volumen (ej: XXX_part001.zip) para encontrar y extraer automáticamente todos los volúmenes del grupo.\nTambién soporta archivos ZIP / 7z / RAR individuales.",
        "pt": "Selecione qualquer arquivo de volume (ex: XXX_part001.zip) para encontrar e extrair automaticamente todos os volumes do grupo.\nTambém suporta arquivos ZIP / 7z / RAR individuais.",
    },
    "label_select_zip": {
        "zh": "选择文件:",
        "zh_TW": "選擇檔案：",
        "en": "Select file:",
        "ja": "ファイル選択:",
        "ko": "파일 선택:",
        "de": "Datei wählen:",
        "fr": "Sélectionner le fichier :",
        "es": "Seleccionar archivo:",
        "pt": "Selecionar arquivo:",
    },
    "hint_select_zip": {
        "zh": "选择 ZIP / 7z / RAR 文件",
        "zh_TW": "選擇 ZIP / 7z / RAR 檔案",
        "en": "Select a ZIP / 7z / RAR file",
        "ja": "ZIP / 7z / RAR ファイルを選択",
        "ko": "ZIP / 7z / RAR 파일을 선택하세요",
        "de": "ZIP / 7z / RAR Datei wählen",
        "fr": "Sélectionner un fichier ZIP / 7z / RAR",
        "es": "Seleccione un archivo ZIP / 7z / RAR",
        "pt": "Selecione um arquivo ZIP / 7z / RAR",
    },
    "label_extract_to": {
        "zh": "解压到:",
        "zh_TW": "解壓到：",
        "en": "Extract to:",
        "ja": "解凍先:",
        "ko": "압축 해제 위치:",
        "de": "Entpacken nach:",
        "fr": "Extraire vers :",
        "es": "Extraer a:",
        "pt": "Extrair para:",
    },
    "hint_extract_to": {
        "zh": "选择解压目标目录",
        "zh_TW": "選擇解壓目標目錄",
        "en": "Select extraction destination",
        "ja": "解凍先ディレクトリを選択",
        "ko": "압축 해제 대상 디렉토리를 선택하세요",
        "de": "Zielverzeichnis zum Entpacken wählen",
        "fr": "Sélectionner le dossier de destination",
        "es": "Seleccione el directorio de destino",
        "pt": "Selecione o diretório de destino",
    },
    "group_unpack_password": {
        "zh": "密码（如果压缩包有密码）",
        "zh_TW": "密碼（如果壓縮檔有密碼）",
        "en": "Password (if the archive is encrypted)",
        "ja": "パスワード（暗号化されている場合）",
        "ko": "비밀번호 (암호화된 경우)",
        "de": "Passwort (falls das Archiv verschlüsselt ist)",
        "fr": "Mot de passe (si l'archive est chiffrée)",
        "es": "Contraseña (si el archivo está cifrado)",
        "pt": "Senha (se o arquivo estiver criptografado)",
    },
    "hint_unpack_password": {
        "zh": "留空则不使用密码",
        "zh_TW": "留空則不使用密碼",
        "en": "Leave empty if no password",
        "ja": "パスワードなしの場合は空欄",
        "ko": "비밀번호가 없으면 비워두세요",
        "de": "Leer lassen wenn kein Passwort",
        "fr": "Laisser vide si pas de mot de passe",
        "es": "Dejar vacío si no hay contraseña",
        "pt": "Deixe vazio se não houver senha",
    },
    "btn_start_unpack": {
        "zh": "▶ 开始解压",
        "zh_TW": "▶ 開始解壓",
        "en": "▶ Start Extracting",
        "ja": "▶ 解凍開始",
        "ko": "▶ 압축 해제 시작",
        "de": "▶ Entpacken starten",
        "fr": "▶ Démarrer l'extraction",
        "es": "▶ Iniciar extracción",
        "pt": "▶ Iniciar extração",
    },
    "log_placeholder": {
        "zh": "日志将显示在这里...",
        "zh_TW": "日誌將顯示在這裡...",
        "en": "Logs will appear here...",
        "ja": "ログがここに表示されます...",
        "ko": "로그가 여기에 표시됩니다...",
        "de": "Protokolle werden hier angezeigt...",
        "fr": "Les journaux s'afficheront ici...",
        "es": "Los registros aparecerán aquí...",
        "pt": "Os registros aparecerão aqui...",
    },
    "msg_select_source": {
        "zh": "请选择有效的源文件夹。",
        "zh_TW": "請選擇有效的來源資料夾。",
        "en": "Please select a valid source folder.",
        "ja": "有効なソースフォルダを選択してください。",
        "ko": "유효한 소스 폴더를 선택하세요.",
        "de": "Bitte wählen Sie einen gültigen Quellordner.",
        "fr": "Veuillez sélectionner un dossier source valide.",
        "es": "Seleccione una carpeta de origen válida.",
        "pt": "Selecione uma pasta de origem válida.",
    },
    "msg_select_output": {
        "zh": "请选择输出目录。",
        "zh_TW": "請選擇輸出目錄。",
        "en": "Please select an output folder.",
        "ja": "出力先を選択してください。",
        "ko": "출력 폴더를 선택하세요.",
        "de": "Bitte wählen Sie einen Ausgabeordner.",
        "fr": "Veuillez sélectionner un dossier de sortie.",
        "es": "Seleccione una carpeta de salida.",
        "pt": "Selecione uma pasta de saída.",
    },
    "msg_select_zip": {
        "zh": "请选择有效的 ZIP 文件。",
        "zh_TW": "請選擇有效的 ZIP 檔案。",
        "en": "Please select a valid ZIP file.",
        "ja": "有効なZIPファイルを選択してください。",
        "ko": "유효한 ZIP 파일을 선택하세요.",
        "de": "Bitte wählen Sie eine gültige ZIP-Datei.",
        "fr": "Veuillez sélectionner un fichier ZIP valide.",
        "es": "Seleccione un archivo ZIP válido.",
        "pt": "Selecione um arquivo ZIP válido.",
    },
    "msg_hint": {
        "zh": "提示",
        "zh_TW": "提示",
        "en": "Notice",
        "ja": "通知",
        "ko": "알림",
        "de": "Hinweis",
        "fr": "Avis",
        "es": "Aviso",
        "pt": "Aviso",
    },
    "msg_done": {
        "zh": "完成",
        "zh_TW": "完成",
        "en": "Done",
        "ja": "完了",
        "ko": "완료",
        "de": "Fertig",
        "fr": "Terminé",
        "es": "Hecho",
        "pt": "Concluído",
    },
    "msg_incomplete": {
        "zh": "操作未完成：",
        "zh_TW": "操作未完成：",
        "en": "Operation incomplete: ",
        "ja": "操作が完了しませんでした：",
        "ko": "작업이 완료되지 않았습니다: ",
        "de": "Vorgang unvollständig: ",
        "fr": "Opération incomplète : ",
        "es": "Operación incompleta: ",
        "pt": "Operação incompleta: ",
    },
    "dialog_select_source": {
        "zh": "选择源文件夹",
        "zh_TW": "選擇來源資料夾",
        "en": "Select Source Folder",
        "ja": "ソースフォルダを選択",
        "ko": "소스 폴더 선택",
        "de": "Quellordner wählen",
        "fr": "Sélectionner le dossier source",
        "es": "Seleccionar carpeta de origen",
        "pt": "Selecionar pasta de origem",
    },
    "dialog_select_output": {
        "zh": "选择输出目录",
        "zh_TW": "選擇輸出目錄",
        "en": "Select Output Folder",
        "ja": "出力先を選択",
        "ko": "출력 폴더 선택",
        "de": "Ausgabeordner wählen",
        "fr": "Sélectionner le dossier de sortie",
        "es": "Seleccionar carpeta de salida",
        "pt": "Selecionar pasta de saída",
    },
    "dialog_select_zip": {
        "zh": "选择压缩文件",
        "zh_TW": "選擇壓縮檔",
        "en": "Select Archive File",
        "ja": "アーカイブファイルを選択",
        "ko": "압축 파일 선택",
        "de": "Archivdatei wählen",
        "fr": "Sélectionner le fichier archive",
        "es": "Seleccionar archivo comprimido",
        "pt": "Selecionar arquivo compactado",
    },
    "dialog_zip_filter": {
        "zh": "ZIP 文件 (*.zip)",
        "zh_TW": "ZIP 檔案 (*.zip)",
        "en": "ZIP Files (*.zip)",
        "ja": "ZIPファイル (*.zip)",
        "ko": "ZIP 파일 (*.zip)",
        "de": "ZIP-Dateien (*.zip)",
        "fr": "Fichiers ZIP (*.zip)",
        "es": "Archivos ZIP (*.zip)",
        "pt": "Arquivos ZIP (*.zip)",
    },
    "dialog_select_extract": {
        "zh": "选择解压目标目录",
        "zh_TW": "選擇解壓目標目錄",
        "en": "Select Extraction Destination",
        "ja": "解凍先ディレクトリを選択",
        "ko": "압축 해제 대상 선택",
        "de": "Zielverzeichnis zum Entpacken wählen",
        "fr": "Sélectionner le dossier de destination",
        "es": "Seleccionar directorio de destino",
        "pt": "Selecionar diretório de destino",
    },
    "splash_loading": {
        "zh": "正在加载...",
        "zh_TW": "正在載入...",
        "en": "Loading...",
        "ja": "読み込み中...",
        "ko": "로딩 중...",
        "de": "Laden...",
        "fr": "Chargement...",
        "es": "Cargando...",
        "pt": "Carregando...",
    },
    "splash_subtitle": {
        "zh": "分卷独立解压打包工具",
        "zh_TW": "分卷獨立解壓打包工具",
        "en": "Volume Packer with Independent Extraction",
        "ja": "分割独立解凍パッカー",
        "ko": "분할 독립 압축 해제 도구",
        "de": "Volumen-Packer mit unabhängiger Extraktion",
        "fr": "Empaqueteur par volumes",
        "es": "Empaquetador por volúmenes",
        "pt": "Empacotador por volumes",
    },
    "compression_store": {
        "zh": "仅存储 (最快)",
        "zh_TW": "僅儲存 (最快)",
        "en": "Store only (fastest)",
        "ja": "格納のみ (最速)",
        "ko": "저장만 (가장 빠름)",
        "de": "Nur speichern (schnellste)",
        "fr": "Stockage seul (le plus rapide)",
        "es": "Solo almacenar (más rápido)",
        "pt": "Apenas armazenar (mais rápido)",
    },
    "compression_fast": {
        "zh": "快速压缩",
        "zh_TW": "快速壓縮",
        "en": "Fast compression",
        "ja": "高速圧縮",
        "ko": "빠른 압축",
        "de": "Schnelle Komprimierung",
        "fr": "Compression rapide",
        "es": "Compresión rápida",
        "pt": "Compressão rápida",
    },
    "compression_normal": {
        "zh": "标准压缩",
        "zh_TW": "標準壓縮",
        "en": "Normal compression",
        "ja": "標準圧縮",
        "ko": "표준 압축",
        "de": "Normale Komprimierung",
        "fr": "Compression standard",
        "es": "Compresión estándar",
        "pt": "Compressão padrão",
    },
    "compression_max": {
        "zh": "最大压缩 (最慢)",
        "zh_TW": "最大壓縮 (最慢)",
        "en": "Maximum compression (slowest)",
        "ja": "最大圧縮 (最遅)",
        "ko": "최대 압축 (가장 느림)",
        "de": "Maximale Komprimierung (langsamste)",
        "fr": "Compression maximale (la plus lente)",
        "es": "Compresión máxima (más lento)",
        "pt": "Compressão máxima (mais lento)",
    },
    "unpack_formats": {
        "zh": "支持格式:",
        "zh_TW": "支援格式:",
        "en": "Supported formats:",
        "ja": "対応形式:",
        "ko": "지원 형식:",
        "de": "Unterstützte Formate:",
        "fr": "Formats supportés :",
        "es": "Formatos soportados:",
        "pt": "Formatos suportados:",
    },
    "msg_select_archive": {
        "zh": "请选择有效的压缩文件（ZIP / 7z / RAR）。",
        "zh_TW": "請選擇有效的壓縮檔（ZIP / 7z / RAR）。",
        "en": "Please select a valid archive file (ZIP / 7z / RAR).",
        "ja": "有効なアーカイブファイル（ZIP / 7z / RAR）を選択してください。",
        "ko": "유효한 압축 파일(ZIP / 7z / RAR)을 선택하세요.",
        "de": "Bitte wählen Sie eine gültige Archivdatei (ZIP / 7z / RAR).",
        "fr": "Veuillez sélectionner un fichier archive valide (ZIP / 7z / RAR).",
        "es": "Seleccione un archivo comprimido válido (ZIP / 7z / RAR).",
        "pt": "Selecione um arquivo compactado válido (ZIP / 7z / RAR).",
    },
}

# 当前语言
_current_lang = "zh"


def detect_system_language() -> str:
    """检测系统语言，返回语言代码"""
    try:
        sys_locale = locale.getdefaultlocale()[0] or ""
        # Check for Traditional Chinese variants first
        locale_lower = sys_locale.lower().replace("-", "_")
        if locale_lower.startswith("zh"):
            if any(tag in locale_lower for tag in ("hant", "tw", "hk", "mo")):
                return "zh_TW"
            return "zh"
        lang_code = sys_locale.split("_")[0].lower()
        if lang_code in ("en",):
            return "en"
        elif lang_code in ("ja",):
            return "ja"
        elif lang_code in ("ko",):
            return "ko"
        elif lang_code in ("de",):
            return "de"
        elif lang_code in ("fr",):
            return "fr"
        elif lang_code in ("es",):
            return "es"
        elif lang_code in ("pt",):
            return "pt"
    except (AttributeError, IndexError, TypeError, ValueError):
        return "en"
    return "en"


def set_language(lang_code: str):
    """设置当前语言"""
    global _current_lang
    if lang_code in ("zh", "zh_TW", "en", "ja", "ko", "de", "fr", "es", "pt"):
        _current_lang = lang_code


def get_language() -> str:
    """获取当前语言代码"""
    return _current_lang


def t(key: str) -> str:
    """获取翻译文本"""
    texts = TEXTS.get(key, {})
    return texts.get(_current_lang, texts.get("en", key))
