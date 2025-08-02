import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";

function HelloPage() {
  return (
    <div>
      <p>你好，这是一个测试页面。</p>
    </div>
  );
}

export default HelloPage;

/*
function BookPage() {
  //把函数功能实体化
  //提取本地数据的函数
  const location = useLocation();
  //跳转网页的函数
  const navigate = useNavigate();

  // 拿到search页传递的db数据
  const dbData = location.state?.dbData;

  // 2️⃣ 防止用户直接访问 /book?q=xxx 而没有 dbData
  if (!dbData) {
    return (
      <div>
        <p>数据已丢失，请返回首页重新搜索。</p>
        <button onClick={() => navigate("/")}>返回首页</button>
      </div>
    );
  }

  // 3️⃣ 准备 Goodreads 相关状态
  const [grData, setGrData] = useState(null);
  const [grLoading, setGrLoading] = useState(true);
  const [grError, setGrError] = useState(null);

  // 4️⃣ 发起 GR 请求（可重复刷新）
  const fetchGrData = async () => {
    try {
      const res = await axios.get(`/api/book/gr/?q=${dbData.en_version_isbn}`);
      const result = res.data.gr_result;
      setGrData(result);
      setGrLoading(result.success === null); // 如果没抓完就继续 loading
    } catch (err) {
      console.error("Goodreads 请求失败:", err);
      setGrError("Goodreads 加载失败，请稍后重试");
      setGrLoading(false);
    }
  };

  // 5️⃣ 页面加载时先请求一次 GR
  useEffect(() => {
    if (dbData?.en_version_url) {
      fetchGrData();
    }
  }, [dbData]);

  // 6️⃣ 如果 GR 没成功提取，1 秒后刷新一次
  useEffect(() => {
    if (grData && grData.success === null) {
      const timer = setTimeout(() => {
        fetchGrData();
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [grData]);

  // 7️⃣ 页面初步渲染测试
  return (
    <div>
      <h2>豆瓣数据</h2>
      <p>书名：{dbData.title}</p>

      <h2>Goodreads 数据</h2>
      {grLoading && <p>正在加载 Goodreads 数据...</p>}
      {grError && <p>{grError}</p>}
      {grData && grData.success && (
        <div>
          <p>英文书名：{grData.gr_book_info.title}</p>
        </div>
      )}
    </div>
  );
}

export default BookPage;
*/
