import { motion, AnimatePresence } from "framer-motion";

export default function SearchLayout({
  inputValue,
  onInputChange,
  onSearch,
  showError,
  errorMessage,
  setShowError,
  isLoading,
}) {
  return (
    <div className="flex items-center justify-cente p-4">
      {/* 整个页面容器 内部纵向间距4*/}
      <div className="w-full mt-[33vh] space-y-4">
        {/* 搜索区域 横向步距 间距8px*/}
        <form
          onSubmit={(e) => {
            e.preventDefault(); // 阻止浏览器刷新页面
            onSearch(); // 调用你已有的搜索函数
          }}
          className="flex mx-auto gap-2"
        >
          {/* 搜索输入区 */}
          <input
            type="text"
            enterKeyHint="search" // ✅ 显示“搜索”或“前往”
            inputMode="search" // ✅ 控制软键盘行为
            placeholder="请输入关键词"
            value={inputValue} // 输入框内容绑定 query
            onChange={onInputChange} // 输入框变化时触发 handleInputChange
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                onSearch();
              }
            }}
            className="w-full mx-auto block border-2 border-gray-300 px-4 py-3 rounded-full text-base placeholder:text-lg" //搜索框样式
          />
        </form>
        <div>
          {/* 顶部输入提示 */}
          <p className="text-lg text-gray-600 leading-relaxed">
            请输入书籍名称，为了精准定位,可输入作者、出版社、出版年份等信息。
          </p>
        </div>
        {/* 正在loading的标识*/}
        {isLoading && (
          <div className="flex justify-center mt-4">
            <div className="w-6 h-6 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
          </div>
        )}
      </div>

      {/* 4. 错误弹窗：只有 showError 为 true 时才显示 加渐变效果*/}
      {showError && (
        <motion.div
          // 初始时透明
          initial={{ opacity: 0 }}
          // 显示时渐变到完全可见
          animate={{ opacity: 1 }}
          // 动画时长为 0.3 秒
          transition={{ duration: 0.3 }}
          // 点击遮罩关闭弹窗
          className="fixed inset-0 z-40 bg-black/70 flex items-center justify-center"
          onClick={() => setShowError(false)} // 点击遮罩关闭
        >
          <div
            className="bg-gray-100/95 w-[66%] h-[20vh] flex items-center justify-center text-center rounded-3xl shadow-2xl shadow-black/60 drop-shadow-lg"
            onClick={(e) => e.stopPropagation()} // 阻止冒泡，点击弹窗本身不关闭
          >
            <p className="px-4 text-lg">{errorMessage}</p>
          </div>
        </motion.div>
      )}
    </div>
  );
}
