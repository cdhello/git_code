macro CreateBlankString(nBlankCount)
{
    szBlank=""
    nIdx = 0
    while(nIdx < nBlankCount)
    {
        szBlank = cat(szBlank," ")
        nIdx = nIdx + 1
    }
    return szBlank
}

macro GetLeftBlank(szLine)
{
    nIdx = 0
    nEndIdx = strlen(szLine)
    while( nIdx < nEndIdx )
    {
        if( (szLine[nIdx] !=" ") && (szLine[nIdx] !="\t") )
        {
            break;
        }
        nIdx = nIdx + 1
    }
    return nIdx
}

macro AskAndSetMyName()
{
    szMyName = Ask("Enter your name:");
    setreg(MYNAME, szMyName);
    return szMyName
}

macro GetMyName()
{
    szMyName = getreg(MYNAME)
    if(strlen( szMyName ) == 0)
    {
        szMyName = AskAndSetMyName()
    }

    return szMyName
}

macro GetDate()
{
    SysTime = GetSysTime(1)
    szy=SysTime.Year
    szm=SysTime.month
    szd=SysTime.day

    return "@szy@/@szm@/@szd@"
}

macro GetFileShortName(szFullName)
{
    len = strlen(szFullName);

    //Msg(szFullName);
    /* 从最后开始找斜杠，该斜杠前面就是路径名，后面就是文件名 */
    i = len
    while  (szFullName[i] != "\\")
    {
        i = i-1;

        /* 有可能全名没有路径名，如刚刚创建还没有保存的文件 */
        if (i < 0)
        {
            break;
        }
    }

    /* 把名字复制出来 */
    szFileName = strmid (szFullName, i + 1, len);

    return szFileName;
}

macro GetFilePath(szFullName)
{
    /* 获取不含路径的文件名 */
    szShortName = GetFileShortName(szFullName);

    LongLen = strlen(szFullName);
    ShortLen = strlen(szShortName);

    /* 把路径复制出来 */
    szFilePath = strmid (szFullName, 0, LongLen - ShortLen);

    return szFilePath
}

/* 获取扩展名 */
macro GetFileExtension(szFullName)
{
    len = strlen(szFullName);

    i = len
    while  (szFullName[i] != ".")
    {
        i = i-1;

        /* 防止没有点 */
        if (i < 0)
        {
            break;
        }
    }

    /* 把扩展名复制出来 */
    szFileExtension = strmid (szFullName, i + 1, len);

    return szFileExtension
}

/* 以上为内部函数 */

macro QSetMyName()
{
    AskAndSetMyName();
}

macro QAddPromblemNo()
{
    pno = ASK("Please Input problem number ");
    SetReg ("PNO", pno);

    des = ASK("Please Input problem description ");
    SetReg ("DES", des);
    
    return szQuestion
}

macro QInsertReviseAdd()
{
    hwnd = GetCurrentWnd();
    sel = GetWndSel(hwnd)
    hbuf = GetCurrentBuf()
    lnMax = GetBufLineCount(hbuf)
    language = getreg(LANGUAGE)
    if(language != 1)
    {
        language = 0
    }
    
    szMyName = GetMyName()
    szDate = GetDate()
    
    SysTime = GetSysTime(1)
    sz=SysTime.Year
    sz1=SysTime.month
    sz3=SysTime.day
    if(sel.lnFirst == sel.lnLast && sel.ichFirst == sel.ichLim)
    {
        szLeft = CreateBlankString(sel.ichFirst)
    }
    else
    {
        szLine = GetBufLine(hbuf, sel.lnFirst)    
        nLeft = GetLeftBlank(szLine)
        szLeft = strmid(szLine,0,nLeft);
    }
    
    szPN = GetReg ("PNO");
    szDES = GetReg ("DES");

    InsBufLine(hbuf, sel.lnFirst, "@szLeft@/* BEGIN: Added by @szMyName@, @szDate@ DES:@szDES@ PN:@szPN@ */");

    if(sel.lnLast < lnMax - 1)
    {
        InsBufLine(hbuf, sel.lnLast + 2, "@szLeft@/* END:   Added by @szMyName@, @szDate@ */");            
    }
    else
    {
        AppendBufLine(hbuf, "@szLeft@/* END:   Added by @szMyName@, @szDate@ */");                        
    }
    SetBufIns(hbuf,sel.lnFirst + 1,strlen(szLeft))
}

macro QInsertReviseDel()
{
    hwnd = GetCurrentWnd()
    sel = GetWndSel(hwnd)
    hbuf = GetCurrentBuf()
    lnMax = GetBufLineCount(hbuf)
    language = getreg(LANGUAGE)
    if(language != 1)
    {
        language = 0
    }

    szMyName = GetMyName()
    szDate = GetDate()
    
    if(sel.lnFirst == sel.lnLast && sel.ichFirst == sel.ichLim)
    {
        szLeft = CreateBlankString(sel.ichFirst)
    }
    else
    {
        szLine = GetBufLine( hbuf, sel.lnFirst )    
        nLeft = GetLeftBlank(szLine)
        szLeft = strmid(szLine,0,nLeft);
    }
    
    szPN = GetReg ("PNO");
    szDES = GetReg ("DES");

    op = Ask("Delete OP? 0: delete, 1: #if 0");

    if (op == 0) /* 直接删除 */
    {
        lineCount = sel.lnLast - sel.lnFirst + 1;

        while (lineCount > 0)
        {
            DelBufLine (hbuf, sel.lnFirst);
            lineCount = lineCount - 1;
        }

        InsBufLine(hbuf, sel.lnFirst, "@szLeft@/* Deleted by @szMyName@, @szDate@ DES:@szDES@ PN:@szPN@ */");

        SetBufIns(hbuf, sel.lnFirst, strlen(szLeft))
    }
    else  /* 使用#if 0删除 */
    {
        InsBufLine(hbuf, sel.lnFirst, "@szLeft@/* BEGIN: Deleted by @szMyName@, @szDate@ DES:@szDES@ PN:@szPN@ */");
        InsBufLine(hbuf, sel.lnFirst + 1, "@szLeft@#if 0");

        if(sel.lnLast < lnMax - 1)
        {
            InsBufLine(hbuf, sel.lnLast + 3, "@szLeft@#endif");
            InsBufLine(hbuf, sel.lnLast + 4, "@szLeft@/* END:   Deleted by @szMyName@, @szDate@ DES:@szDES@ PN:@szPN@ */");
            
        }
        else
        {
            AppendBufLine(hbuf, "@szLeft@#endif"); 
            AppendBufLine(hbuf, "@szLeft@/* END:   Deleted by @szMyName@, @szDate@ */");
        }

        SetBufIns(hbuf,sel.lnFirst + 1,strlen(szLeft))
    }
}

macro QInsertReviseMod()
{
    hwnd = GetCurrentWnd()
    sel = GetWndSel(hwnd)
    hbuf = GetCurrentBuf()
    lnMax = GetBufLineCount(hbuf)
    language = getreg(LANGUAGE)
    if(language != 1)
    {
        language = 0
    }

    szMyName = GetMyName()
    szDate = GetDate()
    
    if(sel.lnFirst == sel.lnLast && sel.ichFirst == sel.ichLim)
    {
        szLeft = CreateBlankString(sel.ichFirst)
    }
    else
    {
        szLine = GetBufLine(hbuf, sel.lnFirst )    
        nLeft = GetLeftBlank(szLine)
        szLeft = strmid(szLine,0,nLeft);
    }
    
    szPNO = GetReg ("PNO");
    szDES = GetReg ("DES");

    InsBufLine(hbuf, sel.lnFirst, "@szLeft@/* BEGIN: Modified by @szMyName@, @szDate@ DES:@szDES@ PN:@szPNO@ */");

    if(sel.lnLast < lnMax - 1)
    {
        InsBufLine(hbuf, sel.lnLast + 2, "@szLeft@/* END:   Modified by @szMyName@, @szDate@ */");         
    }
    else
    {
        AppendBufLine(hbuf, "@szLeft@/* END:   Modified by @szMyName@, @szDate@ */");                        
    }
    
    SetBufIns(hbuf,sel.lnFirst + 1,strlen(szLeft))
}

macro AddCComments(hwnd, sel, hbuf)
{
    if ((sel.lnFirst == sel.lnLast) && (sel.ichFirst == sel.ichLim))
    {
        szLine = GetBufLine(hbuf, sel.lnFirst);
        SetBufSelText(hbuf, "/*  */");
        SetBufIns(hbuf, sel.lnFirst, sel.ichFirst + 3); /* 光标注释符中间，可以直接输入注释内容了 */
    }
    else
    {
        i = sel.lnFirst
        while (i <= sel.lnLast)
        {
            szline = GetBufLine (hbuf, i)
            szline = cat("/*", szline)
            szline = cat(szline, " */")

            InsBufLine(hbuf, i, szline); 
            DelBufLine(hbuf, i + 1)

            i = i + 1
        }

        SetWndSel(hwnd, sel)
    }
}

macro AddPyComments(hwnd, sel, hbuf)
{
    //Msg("py file, to be implemented");

    if ((sel.lnFirst == sel.lnLast) && (sel.ichFirst == sel.ichLim))
    {
        szLine = GetBufLine(hbuf, sel.lnFirst);
        SetBufSelText(hbuf, "#");
        SetBufIns(hbuf, sel.lnFirst, sel.ichFirst + 1);
    }
    else
    {
        i = sel.lnFirst
        while (i <= sel.lnLast)
        {
            szline = GetBufLine (hbuf, i)
            szline = cat("#", szline)

            InsBufLine(hbuf, i, szline); 
            DelBufLine(hbuf, i + 1)

            i = i + 1
        }

        SetWndSel(hwnd, sel)
    }

    return;
}

macro QAddComments()
{
    hwnd = GetCurrentWnd()
    sel = GetWndSel(hwnd)
    hbuf = GetCurrentBuf();

    /* 扩展名 */
    szFileExtension = GetFileExtension(GetBufName (hbuf))

    /* 转为小写 */
    szFileExtension = tolower (szFileExtension)

    if (("c" == szFileExtension) || ("h" == szFileExtension) || ("cpp" == szFileExtension) || ("hpp" == szFileExtension))
    {
        AddCComments(hwnd, sel, hbuf)
    }
    else if ("py" == szFileExtension)
    {
        AddPyComments(hwnd, sel, hbuf)
    }
}

macro DelCComments(hwnd, sel, hbuf)
{
    i = sel.lnFirst
    while (i <= sel.lnLast)
    {
        szline = GetBufLine (hbuf, i)

        if (("/*" == strmid(szline, 0, 2)) && (" */" == strmid(szline, strlen(szline) - 3, strlen(szline))))
        {
            szline = strmid(szline, 2, strlen(szline) - 3)

            InsBufLine(hbuf, i, szline); 
            DelBufLine(hbuf, i + 1)
        }

        i = i + 1
    }

    SetWndSel(hwnd, sel)

    return;
}

macro DelPyComments(hwnd, sel, hbuf)
{
    i = sel.lnFirst
    while (i <= sel.lnLast)
    {
    szline = GetBufLine (hbuf, i)

    if ("#" == szline[0])
    {
        szline = strmid(szline, 1, strlen(szline))

        InsBufLine(hbuf, i, szline); 
        DelBufLine(hbuf, i + 1)
    }

    i = i + 1
    }

    SetWndSel(hwnd, sel)

    return;
}

macro QDelComments()
    {
    hwnd = GetCurrentWnd()
    sel = GetWndSel(hwnd)
    hbuf = GetCurrentBuf();

    /* 扩展名 */
    szFileExtension = GetFileExtension(GetBufName (hbuf))

    /* 转为小写 */
    szFileExtension = tolower (szFileExtension)

    if (("c" == szFileExtension) || ("h" == szFileExtension) || ("cpp" == szFileExtension) || ("hpp" == szFileExtension))
    {
        DelCComments(hwnd, sel, hbuf)
    }
    else if ("py" == szFileExtension)
    {
        DelPyComments(hwnd, sel, hbuf)
    }

    return
}

macro QNewQuotationMark()
{
    hwnd = GetCurrentWnd()
    sel = GetWndSel(hwnd)
    hbuf = GetCurrentBuf();
    QuotationMark = "\"\"";

    //Msg(QuotationMark);

    szLine = GetBufLine(hbuf, sel.lnFirst);

    SetBufSelText(hbuf, QuotationMark);

    SetBufIns(hbuf, sel.lnFirst, sel.ichFirst + 1); /* 光标注释符中间，可以直接输入内容了 */
}

/* 添加文件头 */
macro QFileHeader(hbuf, sel)
{
    hbuf = GetCurrentBuf();

    szMyName = GetMyName()
    szDate = GetDate()

    DelBufLine (hbuf, sel.lnFirst);

    /*  Buf name 就是当前文件包含路径的全名 */
    szBufName = GetBufName (hbuf)

    szFileName = GetFileShortName(szBufName);

    lineNum = 0;
    InsBufLine(hbuf, lineNum, "/*************************************************");lineNum = lineNum + 1;
    InsBufLine(hbuf, lineNum, " *        File Name   : @szFileName@");lineNum = lineNum + 1;
    InsBufLine(hbuf, lineNum, " *        Auhor       : @szMyName@");lineNum = lineNum + 1;
    InsBufLine(hbuf, lineNum, " *        Date        : @szDate@");lineNum = lineNum + 1;
    InsBufLine(hbuf, lineNum, " *        Description : ");lineNum = lineNum + 1;
    InsBufLine(hbuf, lineNum, " *************************************************/");lineNum = lineNum + 1;

    AppendBufLine(hbuf, "");
    AppendBufLine(hbuf, "");
    AppendBufLine(hbuf, "");

    if ("h" == tolower(GetFileExtension(szFileName)) )  /* 头文件 */
    {
        szHeadDef = toupper(szFileName);

        i = 0;
        while(i < strlen(szHeadDef))
        {
            if ("." == szHeadDef[i])
            {
                szHeadDef[i] = "_"
            }

            i = i + 1;
        }

        szHeadDef = "__@szHeadDef@__"

        lineNum = 0;
        InsBufLine(hbuf, lineNum, "#ifndef @szHeadDef@");lineNum = lineNum + 1;
        InsBufLine(hbuf, lineNum, "#define @szHeadDef@");lineNum = lineNum + 1;

        AppendBufLine(hbuf, "#endif /* #ifndef @szHeadDef@ */");
        SetBufIns(hbuf, 6, 25);
    }
    else if("c" == tolower(GetFileExtension(szFileName)) )
    {
        lineNum = 0;
        InsBufLine(hbuf, lineNum, "#ifdef __cplusplus");lineNum = lineNum + 1;
        InsBufLine(hbuf, lineNum, "extern \"C\" {");lineNum = lineNum + 1;
        InsBufLine(hbuf, lineNum, "#endif");lineNum = lineNum + 1;

        AppendBufLine(hbuf, "#ifdef __cplusplus");
        AppendBufLine(hbuf, "} /* extern \"C\"  */");
        AppendBufLine(hbuf, "#endif");
        AppendBufLine(hbuf, "");/* for gcc warning:" no newline at end of file" */

        SetBufIns(hbuf, 7, 25);
    }
}

/* 添加函数头 */
macro QFuncHeader(hbuf, sel)
{
    szMyName = GetMyName()
    szDate = GetDate()

    symbol = GetSymbolLocationFromLn(hbuf, sel.lnFirst)

    if ("" == symbol)
    {
        Msg("Cannot get symbol");
        return;
    }

    funcName = symbol.Symbol;    

    szDeLine = GetBufLine(hbuf, symbol.lnName)    
    szReturn = strmid(szDeLine, 0, symbol.ichName);

    DelBufLine (hbuf, sel.lnFirst);/* 删除原来这一行 */

    lNo = 0;
    InsBufLine(hbuf, sel.lnFirst + lNo, "/*************************************************"); lNo = lNo +1;
    InsBufLine(hbuf, sel.lnFirst + lNo, " * Function   : @funcName@");lNo = lNo +1;
    InsBufLine(hbuf, sel.lnFirst + lNo, " * Description: ");lNo = lNo +1;
    InsBufLine(hbuf, sel.lnFirst + lNo, " * Input      : ");lNo = lNo +1;
    InsBufLine(hbuf, sel.lnFirst + lNo, " * Output     : ");lNo = lNo +1;
    InsBufLine(hbuf, sel.lnFirst + lNo, " * Return     : @szReturn@");lNo = lNo +1;
    InsBufLine(hbuf, sel.lnFirst + lNo, " * Others     : ");lNo = lNo +1;
    InsBufLine(hbuf, sel.lnFirst + lNo, " * Author     : @szMyName@");lNo = lNo +1;
    InsBufLine(hbuf, sel.lnFirst + lNo, " * Date       : @szDate@");lNo = lNo +1;
    InsBufLine(hbuf, sel.lnFirst + lNo, " ************************************************/");lNo = lNo +1;

    SetBufIns(hbuf, sel.lnFirst + 2, 16); 
}

/* 这个用来做一个命令处理，在某行输入几个字符，然后通过快捷键触发这个宏后，可以把那几个字符当命令来作不同处理 */
macro QProcess()
{
    hwnd = GetCurrentWnd()
    hbuf = GetWndBuf(hwnd)
    sel = GetWndSel(hwnd)

    if (sel.lnFirst != sel.lnLast)
    {
        //Msg("chose one line.")
        stop
    }

    szLine = GetBufLine(hbuf, sel.lnFirst);

    if ("func" == szLine)
    {
        QFuncHeader(hbuf, sel);
    }
    else if ("file" == szLine)
    {
        QFileHeader(hbuf, sel);
    }
}

/*
 * 添加一个代码分隔符CODE_SECTION(def) ，可以在左边符号窗口把def的内容显示出来
 * 为了在符号窗口把def显示出来，需要在options->document Options中设置C Source File。Parsing中 C language/Custom Tag/CODE_SECTION("*\(.*\)"*)
 * 为了不加分号就可以识别，需要在C.tom中加一句 CODE_SECTION(def)，否则不加分号SI会认为有一个语句没有结束。
 * 为了能编译通过，需要在代码工程中将CODE_SECTION定义为空: #define CODE_SECTION(def) 
 */
macro QAddCodeSection()
{
    hbuf = GetCurrentBuf();
    hwnd = GetCurrentWnd();
    sel = GetWndSel(hwnd);

    szDes = Ask("Descripion:");

    InsBufLine(hbuf, sel.lnFirst, "CODE_SECTION(@szDes@)");
}

macro QOpenCurDir()
{
    hbuf = GetCurrentBuf();

    /*  Buf name is the cur file s full name */
    szFullName = GetBufName (hbuf)

    /* Use the explorer with para '/select', open the file dir and select it */
    RunCmdLine("explorer /select, @szFullName@", NIL, 0);
}

macro QAddLink()
{
    hwnd = GetCurrentWnd()
    hsrcbuf = GetWndBuf(hwnd)
    sel = GetWndSel(hwnd)
    szsrcfilename = GetFileShortName(GetBufName(hsrcbuf))
    srcfileln = sel.lnFirst

    /* 使用"links", 如果已有直接使用，如果没有新建 */
    linkFilebuf = GetBufHandle("links");
    if (hNil == linkFilebuf)
    {
        linkFilebuf = NewBuf ("links")
        if (hNil == linkFilebuf)   
        {
            Msg("faild.")
            return;
        }
        NewWnd(linkFilebuf)
        SetCurrentWnd(hwnd)
    }             

    szbufline = GetBufLine (hsrcbuf, srcfileln)
    AppendBufLine(linkFilebuf, "@szsrcfilename@(@srcfileln@):@szbufline@");

    desfileln = GetBufLineCount(linkFilebuf) 
    //Msg("line @desfileln@.")

    //SetSourceLink (hsrcbuf, srcfileln, "links", desfileln-1); 
  
    /* 临时文件指向src文件较好，这样临时文件不保存关闭后，link就会删除 */
    SetSourceLink (linkFilebuf, desfileln-1, szsrcfilename, srcfileln);
}

macro QCopyCurFileName()
{
    hbuf = GetCurrentBuf();

    /*  Buf name is the cur file s full name */
    szFullName = GetBufName (hbuf)

    hbufClip = GetBufHandle("Clipboard")
    ClearBuf(hbufClip)
    AppendBufLine(hbufClip, szFullName)  
    //Msg(szFullName);
}
