import React, { useRef, useEffect, useState } from "react";
import { ChevronLeft } from "lucide-react";
import doubanIcon from "../pics/douban.svg";
import goodreadsIcon from "../pics/goodreads.svg";
import {
  getTabButtonClass,
  ScoreTabButton,
  createSetTabAction,
  BookSection,
} from "./BookStyle.jsx";
import { toast } from "react-hot-toast";

export default function BookLayout({
  dbData,
  grData,
  activeTab,
  scrollPositions,
  dispatch,
  modalDispatch,
  modalState,
  onBack,
  query,
}) {
  //弹窗设置
  const { isOpen, modalText } = modalState;
  //每个tab单独滚轮设置
  const scrollRef = useRef(null);
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollPositions[activeTab] || 0;
    }
  }, [activeTab]);
  //控制弹窗
  return (
    <>
      {/* 默认竖向布局占满整个屏幕，避免双滚动条*/}
      <div className="h-screen flex flex-col pt-4">
        {/* 顶部固定容器 */}
        <div className="sticky top-0 left-0 right-0 bg-white z-10">
          {/* 第1行：返回按钮 + query */}
          <div className="flex">
            <button onClick={onBack} className="flex-none text-base pl-3">
              <ChevronLeft className="w-6 h-6 scale-150 text-black " />
            </button>
            <div className="flex-1 flex text-base justify-center ">{query}</div>
          </div>

          {/* 第2行：两个 tab 按钮 */}
          <div className="flex justify-start pt-4">
            <ScoreTabButton
              icon={doubanIcon}
              score={{ platform: "douban", value: dbData?.db_book_info?.score }}
              rating={dbData?.db_book_info?.rating}
              activeTab={activeTab}
              onClick={() => dispatch(createSetTabAction("douban", scrollRef))}
            />
            {/* goodread按钮的三种情况 */}
            {grData?.success === null ? (
              // ✅ 情况1：加载中
              <button
                className={getTabButtonClass("goodreads", activeTab)}
                onClick={() => toast("正在加载中...")}
              >
                <div className="flex text-xl items-center">
                  <img
                    src={goodreadsIcon}
                    className="w-5 h-5 mr-1"
                    alt="Goodreads图标"
                  />
                  <div className="animate-spin h-4 w-4 border-2 border-gray-300 border-t-transparent rounded-full" />
                </div>
              </button>
            ) : grData?.success === false || grData == null ? (
              // ✅ 情况2：加载失败（未找到）
              <button
                className={getTabButtonClass("goodreads", activeTab)}
                onClick={() => toast("未在该平台找到对应书籍")}
              >
                <div className="flex text-xl items-center">
                  <img
                    src={goodreadsIcon}
                    className="w-5 h-5 mr-1"
                    alt="Goodreads图标"
                  />
                  <span>-</span>
                </div>
                <div className="text-sm text-gray-500 mt-1">-人评分</div>
              </button>
            ) : (
              // ✅ 情况3：加载成功，显示评分按钮 + 切换功能
              <ScoreTabButton
                icon={goodreadsIcon}
                score={{
                  platform: "goodreads",
                  value: grData?.gr_book_info?.score,
                }}
                rating={grData?.gr_book_info?.rating}
                activeTab={activeTab}
                onClick={() =>
                  dispatch(createSetTabAction("goodreads", scrollRef))
                }
              />
            )}
          </div>
        </div>
        {/* 主体内容区域（留出顶部空间） */}
        <BookSection
          data={activeTab === "douban" ? dbData : grData}
          scrollRef={scrollRef}
          modalDispatch={modalDispatch}
        />
      </div>
      {/*弹窗 */}
      <div>
        {isOpen && (
          <div className="fixed inset-0 bg-white z-50 flex flex-col">
            <div
              className="flex-1 overflow-y-auto px-4 pb-10 whitespace-pre-line text-lg p-5"
              dangerouslySetInnerHTML={{ __html: modalText }}
            ></div>
            <button
              className="h-[10vh] text-xl px-6 py-3 bg-gray-200 shadow rounded-md text-gray-600"
              onClick={() => modalDispatch({ type: "HIDE_MODAL" })}
            >
              &lt;返回
            </button>
          </div>
        )}
      </div>
    </>
  );
}
