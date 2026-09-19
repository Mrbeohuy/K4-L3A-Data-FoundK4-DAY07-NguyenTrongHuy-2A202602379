# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** RauMa  
**Thành viên:**  
- R1: Trần Phạm Thái Vũ — MSSV: 2A202602695 (Data & Pipeline Lead / Đội trưởng)  
- R2: Nguyễn Tiến Tuân — MSSV: 2A202602595 (Benchmark & Evaluation Lead)  
- R3: Nguyễn Trọng Huy — MSSV: 2A202602379 (Strategy & Architecture Lead)  
**Ngày:** 2026-09-19  

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Chủ đề (Domain) & Lý Do Chọn

**Chủ đề:** Dịch vụ & Quy định Thư viện Đại học (Nội quy mượn trả sách in cho sinh viên và giảng viên, tài liệu số bản quyền, mượn e-Book giáo trình, đặt phòng học nhóm và kiểm tra đạo văn Turnitin) — Thư viện Đại học Ngoại thương (FTU) và Thư viện Học viện Ngoại giao (DAV).

**Tại sao nhóm chọn chủ đề này?**
> Nhóm tập trung 100% vào nghiệp vụ Thư viện Đại học nhằm đáp ứng sâu sắc các ràng buộc cốt lõi của biến thể K4-L3A:
> 1. **Tính phân cấp và đối tượng phục vụ rõ ràng:** Tách biệt rõ chính sách mượn sách giữa Sinh viên (`ftu-library-borrowing-student`: 03 tài liệu/30 ngày) và Giảng viên (`ftu-library-borrowing-faculty`: 05 tài liệu/30 ngày). Đây là cặp tài liệu đối ứng kinh điển để kiểm chứng cơ chế lọc `metadata_filter={"audience": "student"}` phục vụ A/B testing trong Giai đoạn 4.
> 2. **Đầy đủ các loại hình dịch vụ hiện đại:** Bao gồm tài liệu in truyền thống, học liệu số bản quyền (ProQuest, ScienceDirect), sách giáo trình điện tử DRM, dịch vụ giữ chỗ và phòng học nhóm, và dịch vụ học thuật kiểm tra tương đồng văn bản (Turnitin).
> 3. **Độ tin cậy và minh bạch nguồn gốc (Provenance):** 100% tài liệu được trích xuất từ các cổng thông tin thư viện đại học công khai (Đại học Ngoại thương FTU và Học viện Ngoại giao DAV), tuân thủ kiểm tra `robots.txt`, không dùng tài liệu nội bộ/thông tin cá nhân và có URL truy cập thực tế (HTTP 200).

### Danh sách tài liệu (Data Inventory)

| # | Tên tài liệu | Nguồn (Source URL) | Ngày lấy / Phiên bản | Số ký tự | Metadata đã gán |
|---|--------------|------------|--------------------|----------|-----------------|
| 1 | Nội quy Thư viện Học viện Ngoại giao (`dav-library-rules.md`) | https://dav.edu.vn/noi-quy-thu-vien-4957/ | 2026-09-18 / not-stated | 2.200 | `audience: all`, `institution: dav`, `dept: library`, `cat: regulation` |
| 2 | Quy định Mượn trả Tài liệu dành cho Cán bộ & Giảng viên FTU (`ftu-library-borrowing-faculty.md`) | https://thuvien.ftu.edu.vn/noi-dung/quy-dinh | 2026-09-18 / not-stated | 1.935 | `audience: faculty`, `institution: ftu`, `dept: library`, `cat: circulation` |
| 3 | Quy định Mượn trả Tài liệu dành cho Sinh viên FTU (`ftu-library-borrowing-student.md`) | https://thuvien.ftu.edu.vn/noi-dung/quy-dinh | 2026-09-18 / not-stated | 1.960 | `audience: student`, `institution: ftu`, `dept: library`, `cat: circulation` |
| 4 | Nội quy Chung và Quy định Sử dụng Không gian Thư viện FTU (`ftu-library-general-regulations.md`) | https://thuvien.ftu.edu.vn/noi-dung/quy-dinh | 2026-09-18 / not-stated | 2.830 | `audience: all`, `institution: ftu`, `dept: library`, `cat: regulation` |
| 5 | Quy định Khai thác Cơ sở Dữ liệu và Học liệu Điện tử (`library-digital-resources.md`) | https://thuvien.ftu.edu.vn/noi-dung/noi-quy-phuc-vu-tai-lieu-so | 2026-09-18 / 2026.1 | 1.759 | `audience: student`, `institution: ftu`, `dept: library`, `cat: digital` |
| 6 | Hướng dẫn Dịch vụ Đọc và Mượn Sách Điện tử Giáo trình (`library-ebook-service.md`) | https://thuvien.ftu.edu.vn/dich-vu/dich-vu-doc-muon-sach-dien-tu | 2026-09-18 / 2026.1 | 1.626 | `audience: student`, `institution: ftu`, `dept: library`, `cat: ebook` |
| 7 | Hướng dẫn Đặt trước Tài liệu và Phòng Thảo luận Nhóm (`library-online-booking.md`) | https://thuvien.ftu.edu.vn/dich-vu/dang-ky-muon-tai-lieu | 2026-09-18 / 2026.1 | 1.740 | `audience: student`, `institution: ftu`, `dept: library`, `cat: service` |
| 8 | Quy trình Tra soát Trùng lặp trên Turnitin cho Người học (`library-similarity-check.md`) | https://thuvien.ftu.edu.vn/dich-vu/tra-soat-trung-lap | 2026-09-18 / 2025-04-22 | 2.158 | `audience: student`, `institution: ftu`, `dept: library`, `cat: research` |

> Số ký tự tính trên phần thân đã làm sạch (không gồm YAML front matter). Các tài liệu 2, 3, 4 được tách từ cùng một trang quy định nguồn theo `audience`: nếu để chung một file `audience: all` thì filter không có gì để lọc, vì hạn mức của sinh viên và giảng viên nằm cạnh nhau trong mục 3b.

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**
- [x] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng và không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ. *(Chỉ có email dịch vụ công khai `trasoatdaovanthuvien@ftu.edu.vn` nằm trong bước 1 của quy trình tra soát; không có email hay số điện thoại cá nhân.)*
- [x] Mỗi tài liệu có `source_url`, `retrieved_at`, `document_version` (hoặc ngày hiệu lực) trong metadata. *(`document_version` lấy từ ngày ghi trên trang hoặc ngày sửa đổi trong metadata trang; nguồn không nêu thì ghi `not-stated`, không tự đặt số hiệu.)*

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho truy xuất (retrieval)? |
|----------------|------|---------------|-------------------------------|
| `doc_id` | String | `ftu-library-borrowing-student` | Định danh duy nhất của văn bản gốc, dùng để gom các chunk con và thực hiện hàm `delete_document`. |
| `title` | String | `Quy định Mượn trả Tài liệu Thư viện dành cho Sinh viên và Học viên FTU` | Tên văn bản giúp LLM hiển thị nguồn trích dẫn rõ ràng trong câu trả lời (Source Traceability). |
| `source_url` | String | `https://dav.edu.vn/noi-quy-thu-vien-4957/` | Địa chỉ nguồn minh bạch để kiểm chứng độ xác thực của dữ liệu và truy vết quy định gốc (HTTP 200 verified). |
| `retrieved_at` | String (YYYY-MM-DD) | `2026-09-18` | Xác định độ mới của dữ liệu, kiểm soát tính thời hiệu của chính sách. |
| `document_version` | String | `2025-04-22` | Phiên bản hiệu lực của văn bản quy định, tránh nhầm lẫn giữa quy chế cũ và mới. |
| `audience` | Enum | `student`, `faculty`, `all` | **Trường cốt lõi:** Phân tách rõ quy định áp dụng cho Sinh viên hay Giảng viên (ví dụ hạn mượn sách 03 cuốn vs 05 cuốn), phục vụ `metadata_filter`. |
| `department` | String | `library` | Cho phép lọc theo đơn vị quản lý chuyên môn để thu hẹp không gian tìm kiếm. |
| `category` | String | `circulation`, `digital`, `regulation`, `research` | Phân loại chủ đề nghiệp vụ để tăng độ chính xác truy xuất theo chuyên đề. |
| `language` | String | `vi` | Định danh ngôn ngữ tài liệu, hỗ trợ mô hình nhúng tiếng Việt hoặc phân luồng xử lý. |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

> Mỗi thành viên thử **một chiến lược khác nhau** trên cùng bộ tài liệu; nhóm tổng hợp và so sánh ở đây.

### Phân tích đường cơ sở (Baseline Analysis)

Chạy `ChunkingStrategyComparator().compare()` trên 3 tài liệu thực tế của bộ dữ liệu (đã bóc tách YAML front matter, `chunk_size=500`):

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| `ftu-library-general-regulations.md` | FixedSizeChunker (`fixed_size`) | 12 | 466.9 | Thấp — có thể cắt ngang mục/quy định hoặc điều khoản nghiêm cấm |
| | SentenceChunker (`by_sentences`) | 12 | 419.4 | Trung bình — giữ câu nhưng không giữ heading cha |
| | RecursiveChunker (`recursive`) | 11 | 456.5 | Khá — ưu tiên đoạn/dòng trước khi cắt nhỏ |
| `library-similarity-check.md` | FixedSizeChunker (`fixed_size`) | 8 | 456.6 | Thấp — dễ tách bảng số liệu Turnitin khỏi tiêu đề |
| | SentenceChunker (`by_sentences`) | 6 | 549.0 | Trung bình — có chunk dài do bảng và câu dài |
| | RecursiveChunker (`recursive`) | 8 | 410.5 | Khá — giữ được nhiều ranh giới Markdown và hàng bảng |
| `dav-library-rules.md` | FixedSizeChunker (`fixed_size`) | 8 | 465.5 | Thấp đến trung bình — không nhận biết cấu trúc nội quy |
| | SentenceChunker (`by_sentences`) | 9 | 373.6 | Trung bình — phù hợp câu ngắn nhưng mất heading |
| | RecursiveChunker (`recursive`) | 9 | 372.6 | Khá — giữ đoạn giờ mở cửa tốt hơn fixed-size |

### Chiến lược của từng thành viên

**Thành viên 1 — Trần Phạm Thái Vũ (R1 — Data & Pipeline Lead / Đội trưởng)**
- **Loại chiến lược:** Fixed-size — `FixedSizeChunker(chunk_size=500, overlap=100)`
- **Mô tả & lý do chọn cho chủ đề này:** Chiến lược cắt đoạn theo kích thước cố định 500 ký tự với độ gối đầu (overlap) 100 ký tự (20%). Lý do chọn là nhằm thiết lập mốc chuẩn kiểm thử (baseline) cơ bản nhất cho cả nhóm, giúp kiểm soát chặt chẽ giới hạn token đầu vào của mô hình embedding và đo lường sự khác biệt khi nâng cấp lên các chiến lược phân đoạn có nhận biết ngữ cảnh (aware of syntax).
- **Điểm mạnh:** Đảm bảo độ dài đồng đều tuyệt đối giữa các chunk, tốc độ xử lý nhanh nhất ($O(N)$ đơn giản), độ gối đầu 100 ký tự hỗ trợ cứu vãn phần nào các cụm từ quan trọng nằm sát biên cắt.
- **Điểm yếu:** Cắt cơ học không quan tâm đến ngữ nghĩa, dễ chém ngang giữa hàng bảng hoặc tách số liệu khỏi điều kiện ràng buộc (ví dụ cụm "Khóa luận tốt nghiệp | 25%" bị đẩy xuống thứ hạng thấp ở Q2).

**Thành viên 2 — Nguyễn Tiến Tuân (R2 — Benchmark & Evaluation Lead)**
- **Loại chiến lược:** Recursive — `RecursiveChunker(chunk_size=400)`, separators mặc định `["\n\n", "\n", ". ", " ", ""]`
- **Mô tả & lý do chọn:** Văn bản quy định sau khi làm sạch có cấu trúc đoạn → dòng (mỗi khoản/dòng bảng một dòng), nên cắt theo `\n\n` rồi `\n` giữ được trọn từng khoản, sau đó gom các dòng liền kề tới sát `chunk_size`. Đã chạy lưới 4 kích thước (300/400/500/800) × 3 bộ separator trên `bench.py` (embedder `paraphrase-multilingual-MiniLM-L12-v2`), chấm Mức 2:

  | Separators | 300 | 400 | 500 | 800 |
  |---|---|---|---|---|
  | mặc định | 4/10 | **5/10** (Q3 hạng 2) | 5/10 (Q3 hạng 3) | 5/10 |
  | + `"\n## ", "\n### "` (md-heading) | 5/10 | 5/10 | 5/10 | 5/10 — nhưng chỉ 3/5 câu có đáp án trong top-3 |
  | + `"; ", ", "` (clause) | giống hệt mặc định — các dòng kết thúc `;` đã bị tách bởi `\n` từ trước |

  Chọn 400: cùng điểm cao nhất, 4/5 câu có đáp án trong top-3, không có chunk vụn 1 ký tự như ở 300 (phần dư của bước cắt cứng). Thêm separator heading làm hỏng Q3 vì tách hàng bảng khỏi phần mô tả quy trình.
- **Điểm yếu quan sát được:** (1) chunk heading lẻ (min 17 ký tự) khi section kế tiếp quá dài; (2) Q1/Q2 luôn ở hạng 2 — chunk đầu file (tiêu đề + câu giới thiệu, *không có số liệu*) giống câu hỏi hơn chunk chứa con số; (3) Q5 không vào top-3 ở mọi cấu hình ≤ 500.

**Thành viên 3 — Nguyễn Trọng Huy (R3 — Strategy & Architecture Lead)**
- **Loại chiến lược:** Custom — `HeadingSectionChunker(max_chunk_size=500)`
- **Mô tả & lý do chọn:** Nhận thấy văn bản quy chế đại học luôn được biên soạn theo cấu trúc phân cấp pháp lý (`# Tiêu đề`, `## Điều/Mục`, `### Khoản`). R3 xây dựng chunker cắt trước theo đề mục Markdown, mỗi section là một chunk độc lập; nếu section vượt quá 500 ký tự sẽ đệ quy cắt nhỏ và **gắn kèm heading breadcrumb** (tiêu đề mục cha) vào đầu mỗi mảnh con để không bao giờ bị mất ngữ cảnh.
- **Code snippet (custom implementation):**
```python
class HeadingSectionChunker:
    HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

    def __init__(self, max_chunk_size: int = 500):
        self.max_chunk_size = max_chunk_size

    def chunk(self, text: str) -> list[str]:
        chunks = []
        for heading_lines, body_lines in self._split_sections(text):
            section = "\n".join([*heading_lines, *body_lines]).strip()
            if len(section) <= self.max_chunk_size:
                chunks.append(section)
            else:
                heading_prefix = "\n".join(heading_lines)
                fallback_size = self.max_chunk_size - len(heading_prefix) - 2
                body = "\n".join(body_lines)
                for child in RecursiveChunker(chunk_size=fallback_size).chunk(body):
                    chunks.append(f"{heading_prefix}\n\n{child}".strip())
        return chunks
```
- **Điểm mạnh:** Bảo toàn 100% ranh giới điều khoản pháp lý, tạo ra 49 chunks (độ dài TB 358 ký tự, min 181, max 498), giải quyết triệt để hiện tượng chunk mất ngữ cảnh khi bị cắt vụn, hiệu quả xuất sắc với các câu hỏi tra cứu theo điều khoản/nghiêm cấm (Q5).
- **Điểm yếu:** Với MockEmbedder, điểm bị ảnh hưởng nhiễu (3/10 doc-level, 1/10 chunk-level); các mục trong cùng một văn bản có độ tương đồng ngữ nghĩa sát nhau nên dễ tranh chấp thứ hạng.

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (Mức 1 / Mức 2) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| **R1 — Trần Phạm Thái Vũ** | FixedSize (`500`, overlap `100`) | Mức 1: **7/10** · Mức 2: **3/10** *(Mock: 1/1)* | Dễ triển khai, kiểm soát chặt chẽ độ dài token, thắng ở câu cấu trúc phẳng (Q4 giờ mở cửa) | Cắt ngang câu/bảng số liệu; điểm Mức 2 thấp do con số bị tách khỏi ngữ cảnh |
| **R2 — Nguyễn Tiến Tuân** | Recursive (`chunk_size=400`) | Mức 1: **9/10** · Mức 2: **5/10** | 4/5 câu có đáp án trong top-3; giữ trọn dòng bảng Turnitin; bắt chính xác Q3 quy trình | Chunk tiêu đề/giới thiệu chiếm hạng 1 thay vì chunk số liệu (Q1, Q2); trượt Q5 |
| **R3 — Nguyễn Trọng Huy** | HeadingSection (Custom, `500`) | Mức 1: **8/10** · Mức 2: **6/10** *(Mock: 3/1)* | Gắn heading cha vào chunk con (TB 358 ký tự); vượt trội ở Q5 (nghiêm cấm) và Q1 (hạn mức) | Các mục trong cùng văn bản có vector embedding khá sát nhau, dễ tranh chấp top-3 |
| *(Tham chiếu)* | Sentence (Baseline, `max=3`) | Mức 1: 7/10 · Mức 2: 6/10 | Thắng Q1 và Q5 nhờ gom các mục cùng chủ đề vào chunk dài | Kích thước chunk không kiểm soát được (TB 443, max 1834 ký tự) vì danh sách/bảng thiếu dấu chấm câu |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> **Chiến lược `RecursiveChunker(chunk_size=400)` (R2) kết hợp nguyên lý của `HeadingSectionChunker` (R3) là tối ưu nhất cho văn bản quy chế đại học.** Lý do là vì quy chế thư viện không phải là văn xuôi tự do mà được cấu trúc hoá cao độ theo từng Mục, Điều, Khoản và Bảng tiêu chuẩn. Việc tôn trọng ranh giới phân tách tự nhiên (`\n\n` cho đoạn, `\n` cho từng dòng danh sách/bảng) giúp toàn bộ điều kiện và con số quy định (như "03 tài liệu/30 ngày" hay "25% Turnitin") nằm trọn vẹn trong một khối ngữ cảnh duy nhất, mang lại độ chính xác truy xuất cao nhất mà không làm vỡ vụn thông tin.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng, có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Đây là bộ câu hỏi chung cho mọi thành viên chạy.

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk nào chứa thông tin? |
|---|-------|-------------------------------|--------------------------|
| 1 | *(bẫy audience — chạy với `metadata_filter={"audience": "student"}`)* Ở Thư viện Đại học Ngoại thương được mượn về nhà tối đa bao nhiêu tài liệu và trong bao lâu? | "03 tài liệu/30 ngày (Một lần gia hạn thêm 15 ngày tính từ ngày thực hiện lệnh gia hạn) đối với sách tham khảo" | `ftu-library-borrowing-student` › *Mục 2. Hạn mức Mượn*. Bẫy: `ftu-library-borrowing-faculty` cùng mục, cùng từ vựng nhưng đáp án là "05 tài liệu/30 ngày" |
| 2 | Chỉ số trùng lặp tối đa cho khóa luận tốt nghiệp khi tra soát trên Turnitin là bao nhiêu? | "Khóa luận tốt nghiệp: 25%" | `library-similarity-check` › *Mục 2. Tiêu chuẩn và Ngưỡng Chỉ số Trùng lặp Turnitin* (bảng) |
| 3 | Sau khi người học nộp biên bản tra soát, thư viện trả kết quả trong bao lâu và ở đâu? | "Trả kết quả tra soát tại K214 (Nhà K – ĐH Ngoại thương), chậm nhất trong vòng 02 ngày làm việc kể từ ngày người học nộp biên bản hợp lệ" | `library-similarity-check` › *Mục 3. Quy trình Thực hiện 7 Bước* (Bước 6) |
| 4 | Thư viện Học viện Ngoại giao mở cửa vào Thứ Bảy từ mấy giờ đến mấy giờ? | "Thứ Bảy: Từ 9:00 đến 18:00 (thông tầm không nghỉ giữa giờ); thư viện dừng phục vụ bạn đọc 15 phút trước giờ đóng cửa" | `dav-library-rules` › *Mục 2. Thời gian Mở cửa (áp dụng từ 01/3/2022)* |
| 5 | Mượn tài liệu về nhà trả trễ hạn bao nhiêu lần trong một năm học thì bị coi là hành vi nghiêm cấm? | "Mượn tài liệu về nhà quá hạn trên 03 lần/năm học" | `ftu-library-general-regulations` › *Mục 4. Các Hành vi Bị Nghiêm cấm tại Thư viện* |

> Đa dạng dạng hỏi: bẫy đối tượng (Q1), tra con số trong bảng (Q2), quy trình/thời hạn (Q3), tra cứu giờ phục vụ của trường đối ứng (Q4), điều kiện vi phạm diễn đạt khác từ gốc — "trả trễ hạn" thay vì "quá hạn" (Q5). Mọi gold answer đã kiểm tra có nguyên văn trong file. Trong `bench.py`, mỗi câu khai báo thêm `needle` — chuỗi con bắt buộc có trong chunk truy xuất — để chấm Mức 2 (chunk chứa đáp án) chứ không chỉ Mức 1 (đúng `doc_id`).

### Tổng hợp chất lượng truy xuất của nhóm

> Cách chấm (theo `docs/SCORING.md`): **2 điểm/câu** — top-3 chứa chunk liên quan + agent trả lời đúng (2), có liên quan nhưng thiếu/không ở top-1 (1), không có trong top-3 (0).

Hạng của chunk chứa đáp án (Mức 2) trên từng chiến lược — cùng corpus, cùng embedder `paraphrase-multilingual-MiniLM-L12-v2`, cùng `bench.py` (— = không có trong top-3):

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú |
|---|---------|-------------------------------|-------------------------------|---------|
| 1 | Hạn mức mượn về nhà (filter student) | Sentence (hạng 1) / Recursive (hạng 2) | Fixed **2** · Sentence **1** · Recursive-400 **2** · Heading **1** | Chunk thắng của Sentence/Heading chứa **cả tiêu đề lẫn con số**; Recursive/Fixed tách tiêu đề + câu giới thiệu thành chunk riêng không có số, và chunk đó đứng hạng 1 |
| 2 | Chỉ số trùng lặp khóa luận | Recursive-400 (R2) / Sentence (hạng 2) | Fixed **—** · Sentence **2** · Recursive-400 **2** · Heading **3** | Fixed vẫn có 2 chunk chứa trọn "Khóa luận tốt nghiệp \| 25%" (nhờ overlap) nhưng chỉ xếp hạng 5 và 7; Recursive và Heading bắt chính xác vào top-3 |
| 3 | Thời hạn & nơi trả kết quả tra soát | Recursive-400 (R2) (hạng 2) | Fixed **—** · Sentence **—** · Recursive-400 **2** · Heading **—** | Câu khó nhất: với Recursive-400, chunk mượn sách "03 tài liệu/30 ngày" đứng top-1 (0.661) — trùng chủ đề "thời hạn", hơn chunk đáp án (0.651) chỉ 0.010 |
| 4 | Giờ mở cửa DAV Thứ Bảy | Fixed / Recursive-400 / Heading (hạng 1) | Fixed **1** · Sentence **3** · Recursive-400 **1** · Heading **1** | Câu dễ: mục giờ mở cửa ngắn, tách biệt rõ ràng, cả Fixed, Recursive và Heading đều đạt điểm tuyệt đối top-1 |
| 5 | Số lần quá hạn bị nghiêm cấm | HeadingSection (R3) / Sentence (hạng 1) | Fixed **—** · Sentence **1** · Recursive-400 **—** · Heading **1** | Câu hỏi dùng "trả trễ hạn" thay cho "quá hạn". HeadingSection gom trọn mục nghiêm cấm kèm heading cha nên đạt top-1; Recursive cắt danh sách ở chỗ khác nên mục này nằm lẫn với mục không liên quan |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> **Có — đóng vai trò quyết định ở Q1.** Chạy thử nghiệm A/B trên cả 4 cấu hình:
> - **Khi KHÔNG lọc (`filter=None`):** Chunk đáp án mượn sách của sinh viên **hoàn toàn không vào được top-3 ở bất kỳ chiến lược nào** (0 điểm Mức 2); có từ 2 đến 3/3 chunk trong top-3 là tài liệu của giảng viên (`ftu-library-borrowing-faculty`) hoặc nội quy chung (`audience: all`). Nguy hiểm nhất là agent sẽ đọc chunk của giảng viên và khẳng định chắc chắn sinh viên được mượn "05 tài liệu/30 ngày" — gây ra hiện tượng ảo giác sai đối tượng (hallucination).
> - **Khi CÓ lọc (`metadata_filter={"audience": "student"}`):** Đáp án của sinh viên lập tức nhảy lên hạng 1–2 (đạt 1–2 điểm Mức 2). Kết quả kiểm chứng thực nghiệm này chứng minh cơ chế tiền lọc (pre-filtering) trong `search_with_filter` là bắt buộc phải có đối với các hệ thống RAG phục vụ nhiều nhóm người dùng khác nhau.

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
> 1. **Chấm 2 mức (Doc-level vs Chunk-level):** Đánh giá theo `doc_id` làm "thổi phồng" chất lượng retrieval từ 2–4 điểm (R2 đạt 9 vs 5, R3 đạt 3 vs 1 trên Mock). Một hệ thống có thể lấy đúng tài liệu nhưng lấy sai đoạn (chỉ lấy phần mở đầu, không có số liệu), khiến LLM không thể trả lời được.
> 2. **Heading Breadcrumb Injection (Phát hiện từ R3):** Việc gắn kèm tiêu đề mục cha vào từng chunk con giúp giải quyết triệt để việc mất ngữ cảnh khi cắt nhỏ section quy định, giúp câu hỏi Q5 đạt hạng 1 tuyệt đối mà các chiến lược khác bị trượt.
> 3. **Sức mạnh và ranh giới của Metadata Pre-filtering:** Không có filter, câu hỏi bẫy đối tượng (Q1) hoàn toàn thất bại. Tuy nhiên, nếu lọc quá cứng (`audience: student`), hệ thống sẽ vô tình loại bỏ các tài liệu quy định chung hữu ích (`audience: all`), đòi hỏi giải pháp hỗ trợ filter danh sách đa giá trị `{"audience": ["student", "all"]}`.

**Bài học rút ra khi so sánh trong nhóm:**
> Khi so sánh cùng một tập dữ liệu trên 3 chiến lược khác nhau, nhóm nhận thấy không có một chiến lược chunking nào vượt trội tuyệt đối trên mọi loại câu hỏi:
> - `FixedSize` (R1) hoạt động tốt trên các văn bản phẳng, đồng nhất nhưng thất bại khi gặp bảng dữ liệu.
> - `Recursive` (R2) cân bằng nhất, xử lý xuất sắc các cấu trúc danh sách và quy trình nhiều bước.
> - `HeadingSection` (R3) bảo toàn ngữ nghĩa pháp lý tốt nhất nhờ cấu trúc breadcrumb.
> Sự phối hợp giữa cấu trúc văn bản nguồn và chiến lược chia nhỏ là yếu tố quyết định chất lượng của toàn bộ đường ống RAG.

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> 1. **Bổ sung metadata phân cấp:** Không chỉ gán `audience`, nhóm sẽ gán thêm trường `content_type` (`table`, `procedure`, `policy`) để hỗ trợ router tự động chọn chiến lược retrieval phù hợp.
> 2. **Chuẩn hóa cấu trúc Markdown trước khi nạp:** Chuyển đổi các bảng biểu phức tạp thành định dạng Key-Value hoặc JSON trước khi chunking để tránh tình trạng hàng tiêu đề bị tách rời khỏi dòng dữ liệu chứa con số.
> 3. **Áp dụng Heading Breadcrumb rộng rãi:** Mọi thành viên nên kế thừa kỹ thuật của R3 để nhúng heading cha vào chunk, thay vì cắt thuần túy cơ học.

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | 10 / 10 |
| Thiết kế chiến lược (Strategy Design) | 15 / 15 |
| Chất lượng truy xuất (Retrieval Quality) | 10 / 10 |
| Thuyết trình (Demo) | 5 / 5 |
| **Tổng phần nhóm** | **40 / 40** |
