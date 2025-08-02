export default function SearchLayout({
  inputValue,
  onInputChange,
  onSearch,
  showError,
  errorMessage,
  setShowError,
}) {
  return (
    <div>
      {/* 整个页面容器 */}
      <div>
        {/* 搜索区域 */}
        <div>
          {/* 搜索输入区 */}
          <input
            type="text"
            placeholder="请输入关键词"
            value={inputValue} // 输入框内容绑定 query
            onChange={onInputChange} // 输入框变化时触发 handleInputChange
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                onSearch();
              }
            }}
          />

          <button onClick={onSearch}>搜索</button>
        </div>
        <div>
          {/* 顶部输入提示 */}
          <p>
            请输入书籍名称，为了精准定位,可输入作者、出版社、出版年份等信息。
          </p>
        </div>
      </div>

      {/* 4. 错误弹窗：只有 showError 为 true 时才显示 */}
      {showError && (
        <div onClick={() => setShowError(false)}>
          <p>{errorMessage}</p>
        </div>
      )}
    </div>
  );
}
