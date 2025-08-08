//react的hook,用来保存用户关键词
import { useState } from "react";
//react router提供的跳转方法
import { useNavigate } from "react-router-dom";

import { useEffect } from "react";
//用来发送http请求
import axios from "axios";
import SearchLayout from "./SearchLayout";
// utils/api.js 或 BookUtils.js 等
const API_BASE = "https://exercise1-book-review.onrender.com/";

//定义一个react组件
//输入关键词后调用后端/api/book/db/?q=？,并返回db的数据，判断。成功则跳转。
function SearchPage() {
  // 输入框内容
  const [query, setQuery] = useState("");
  // 控制弹窗显示
  const [showError, setShowError] = useState(false);
  // 错误内容（比如后台返回的错误信息）
  const [errorMsg, setErrorMsg] = useState("");
  // 路由跳转
  const navigate = useNavigate();
  // 加载是否显示的变量
  const [isLoading, setIsLoading] = useState(false);

  // 输入框变化时触发
  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };
  //弹窗后当前光标失去焦点
  useEffect(() => {
    if (showError) {
      document.activeElement.blur();
    }
  }, [showError]);
  //触发搜所时触发的函数，用async声明
  const handleSearch = async () => {
    document.activeElement.blur(); // ✅ 收起键盘
    setIsLoading(true); // 开始加载动画
    try {
      //用axios发送get请求到后端api，await 表示这里是异步的，等请求返回后再继续往下执行
      const res = await axios.get(
        //encodeURIComponent() 把关键词转成 URL 编码，防止中文或空格出错
        `${API_BASE}/api/book/db/?q=${encodeURIComponent(query)}`
      );
      //从返回的数据中提取db_result
      const dbResult = res.data.db_result;
      //如果sucess是false，则返回失败信息
      if (dbResult.success === false) {
        setErrorMsg(dbResult.error || "搜索失败");
        setShowError(true);
        return;
      }
      //把数据存入本地，防止book页刷新后没数据
      localStorage.setItem("dbData", JSON.stringify(dbResult));
      localStorage.setItem("query", query);

      //成功则执行跳转，，带上关键词作为查询参数传给 BookPage
      navigate(`/book?q=${encodeURIComponent(query)}`);
    } catch (error) {
      console.error(error);
      setErrorMsg("请求失败，请稍后再试");
      setShowError(true);
    } finally {
      setIsLoading(false); // 6️⃣ 不管成功还是失败，最后都关闭加载动画
    }
  };

  return (
    <SearchLayout
      inputValue={query}
      onInputChange={handleInputChange}
      onSearch={handleSearch}
      showError={showError}
      errorMessage={errorMsg}
      setShowError={setShowError}
      isLoading={isLoading}
    />
  );
}

export default SearchPage;
