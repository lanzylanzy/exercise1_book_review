//react的hook,用来保存用户关键词
import { useState } from "react";
//react router提供的跳转方法
import { useNavigate } from "react-router-dom";
//用来发送http请求
import axios from "axios";
import SearchLayout from "./SearchLayout";

//定义一个react组件
//输入关键词后调用后端/api/book/db/?q=？,并返回db的数据，判断。成功则跳转。
function SearchPage() {
  // 1. 输入框内容
  const [query, setQuery] = useState("");
  // 2. 控制弹窗显示
  const [showError, setShowError] = useState(false);
  // 3. 错误内容（比如后台返回的错误信息）
  const [errorMsg, setErrorMsg] = useState("");
  // 4. 路由跳转
  const navigate = useNavigate();

  // 5. 输入框变化时触发
  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  //点击搜所时触发的函数，用async声明
  const handleSearch = async () => {
    try {
      //用axios发送get请求到后端api，await 表示这里是异步的，等请求返回后再继续往下执行
      const res = await axios.get(
        //encodeURIComponent() 把关键词转成 URL 编码，防止中文或空格出错
        `/api/book/db/?q=${encodeURIComponent(query)}`
      );
      //从返回的数据中提取db_result
      const dbResult = res.data.db_result;
      //如果sucess是false，则返回失败信息
      if (dbResult.success === false) {
        setErrorMsg(dbResult.error || "搜索失败");
        setShowError(true);
        return;
      }

      //成功则执行跳转，，带上关键词作为查询参数传给 BookPage
      navigate(`/book?q=${encodeURIComponent(query)}`, {
        state: { dbData: dbResult }, // 将提取的数据存储，方便下一页直接调用
      });
    } catch (error) {
      console.error(error);
      setErrorMsg("请求失败，请稍后再试");
      setShowError(true);
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
    />
  );
}

export default SearchPage;
