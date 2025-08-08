import { useEffect, useState, useReducer } from "react";
import axios from "axios";
import { useLocation, useNavigate } from "react-router-dom";
import BookLayout from "./BookLayout";

//tab逻辑
//tab初始状态
const initialState = {
  activeTab: "douban", // 默认豆瓣
  //滚轮参数
  scrollPositions: {
    douban: 0,
    goodreads: 0,
  },
};
// 关于tap的reducer函数，专门处理状态更新逻辑
function reducer(state, action) {
  switch (action.type) {
    case "SET_TAB":
      return {
        ...state,
        activeTab: action.payload.tab,
        scrollPositions: {
          ...state.scrollPositions,
          [state.activeTab]: action.payload.prevScroll, // 保存当前 tab 的滚动位置
        },
      };
    default:
      return state;
  }
}
//弹窗初始函数
const modalInitial = {
  isOpen: false,
  modalText: "",
};

function modalReducer(state, action) {
  switch (action.type) {
    case "SHOW_MODAL":
      return { isOpen: true, modalText: action.payload };
    case "HIDE_MODAL":
      return { isOpen: false, modalText: "" };
    default:
      return state;
  }
}

export default function BookPage() {
  //初始化两个hook，即两个react的aip，允许用户使用一些功能
  const location = useLocation();
  const navigate = useNavigate();
  // 从上一页拿豆瓣数据
  const dbData = JSON.parse(localStorage.getItem("dbData"));
  //从上一页拿query数据
  const query = localStorage.getItem("query");
  // 增加Goodreads 数据状态变量
  const [grData, setGrData] = useState(null);
  // 使用useReducer来管理 tab 切换状态
  const [state, dispatch] = useReducer(reducer, initialState);
  //使用reducer管理弹窗
  const [modalState, modalDispatch] = useReducer(modalReducer, modalInitial);

  //定义返回上一页的函数
  const handleBack = () => {
    navigate("/"); // 或者用 window.history.back()
  };

  //useEffect是react常用的一个副作用，即页面加载后执行某段逻辑
  // 页面加载后，请求 Goodreads
  useEffect(() => {
    //制作一个后端拉取gr信息的函数fetchgr，设置gr.success未null时每隔0.5s重新拉取数据，直到success
    const fetchGr = () => {
      axios
        .get(`/api/book/gr?en_url=${encodeURIComponent(dbData.en_version_url)}`)
        .then((res) => {
          const result = res.data.gr_result;
          setGrData(result);

          // 如果还没成功，就等 0.5 秒再拉一次
          if (result.success === null) {
            setTimeout(fetchGr, 500);
          }
        });
    };
    //如果en_version_url存在，即执行拉取函数
    if (dbData?.en_version_url) {
      fetchGr();
    }
  }, [dbData?.en_version_url]); //此函数依赖于en_version_url，即en_version_url更新时就重新执行
  return (
    <BookLayout
      dbData={dbData}
      grData={grData}
      activeTab={state.activeTab}
      scrollPositions={state.scrollPositions}
      dispatch={dispatch}
      modalState={modalState}
      modalDispatch={modalDispatch}
      onBack={handleBack}
      query={query}
    />
  );
}
