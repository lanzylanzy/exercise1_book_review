import React from "react";
import { useRef, useEffect, useState } from "react";

//切换tab时滚轮也切换到原tab
export function createSetTabAction(tab, scrollRef) {
  return {
    type: "SET_TAB",
    payload: {
      tab,
      prevScroll: scrollRef?.current?.scrollTop || 0,
    },
  };
}

//上方标签样式
export function getTabButtonClass(tabName, activeTab) {
  const base =
    "w-1/3 px-3 py-1 flex flex-col items-start justify-start  border rounded-t-xl rounded-b-none border-none";
  const active = "bg-white shadow-[2px_-1.5px_2px_0px_rgba(0,0,0,0.1)]";
  const inactive = "bg-gray-100 text-gray-500";

  return `${base} ${tabName === activeTab ? active : inactive}`;
}

//标签内部(通用)
export function ScoreTabButton({ icon, score, rating, activeTab, onClick }) {
  // 判断当前按钮是否为激活状态，用于控制样式
  const isActive = activeTab === score?.platform;

  return (
    <button
      onClick={onClick} // 点击按钮时触发传入的函数
      className={getTabButtonClass(score?.platform, activeTab)} // 动态生成样式类名
    >
      {/* 第一行：图标 + 分数，垂直居中 */}
      <div className="flex text-xl font-semibold items-center">
        <img src={icon} className="w-5 h-5 mr-3" alt="平台图标" />
        {score?.value ?? "-"} {/* 分数显示，若为空则显示 "-" */}
      </div>

      {/* 第二行：评分人数，字体小，灰色，稍微有点边距 */}
      <div className="text-sm text-gray-500">
        {rating ?? "-"}人评分 {/* 人数为空也显示占位符 */}
      </div>
    </button>
  );
}

//评论通用函数
export function ReviewRow({ reviews, title, onClick }) {
  return (
    <div className="mb-3">
      <div className="font-semibold mb-1 text-lg">{title}</div>
      <div className="flex overflow-x-auto text-lg space-x-4 pb-2">
        <div className="flex space-x-4 pb-2">
          {reviews?.map((item, idx) => {
            const rev = Object.values(item)[0]; // 取出评论内容对象
            return (
              <div
                key={idx}
                className="flex flex-col shrink-0 w-[80vw] p-3 text-gray-600 bg-gray-100 rounded-lg shadow"
                onClick={() => onClick(rev.content)} // ✅ 外部传入点击行为
              >
                <p
                  className="text-lg line-clamp-5 mb-2 whitespace-pre-line"
                  dangerouslySetInnerHTML={{ __html: rev.content }}
                ></p>
                <div className="text-sm text-gray-500 mt-auto">
                  评分 {rev.review_score ?? "-"} ⭐ · {rev.date}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

//
export function BookSection({ data, scrollRef, modalDispatch }) {
  const book = data?.db_book_info || data?.gr_book_info; // 自动取对的数据字段
  const goodReviews = data?.db_good_reviews || data?.gr_good_reviews;
  const badReviews = data?.db_bad_reviews || data?.gr_bad_reviews;

  return (
    <div
      ref={scrollRef}
      className="flex overflow-y-auto h-[calc(100vh-0px)] flex-col"
    >
      <div>
        {/* 封面 + 书名等 */}
        <div className="flex items-start gap-4 px-4 pt-6">
          <img
            src={book?.img}
            alt="封面获取失败"
            className="w-[25vw] h-auto rounded-lg shadow-[0_0_15px_2px_rgba(0,0,0,0.2)]"
          />
          <div>
            <h3 className="text-lg font-semibold  mb-1">
              {book?.title || "暂无书名"}
            </h3>
            <p className="text-base text-gray-700 mb-1">
              作者：{book?.author || "未知"}
            </p>
            <p className="text-base text-gray-700">
              出版时间：{book?.published_date || "未知"}
            </p>
          </div>
        </div>

        {/* 简介 */}
        <div className="text-lg text-gray-700 p-4">
          <p className="font-semibold mb-1 mt-3">简介</p>
          <p className="line-clamp-4 overflow-hidden whitespace-pre-line relative">
            {book?.intr || "暂无简介"}

            {book?.intr && (
              <button
                onClick={() =>
                  modalDispatch({
                    type: "SHOW_MODAL",
                    payload: book.intr,
                  })
                }
                className="bg-white text-blue-600 text-lg absolute bottom-0 right-0 leading-none mb-1 mr-0.5 pt-1"
              >
                ...更多
              </button>
            )}
          </p>
        </div>

        {/* 评论 */}
        <div className="px-4 mt-3">
          <ReviewRow
            reviews={goodReviews}
            title="好评"
            onClick={(content) =>
              modalDispatch({ type: "SHOW_MODAL", payload: content })
            }
          />
          <ReviewRow
            reviews={badReviews}
            title="差评"
            onClick={(content) =>
              modalDispatch({ type: "SHOW_MODAL", payload: content })
            }
          />
        </div>

        {/* 底部留白 */}
        <div className="h-[20vh]"></div>
      </div>
    </div>
  );
}
