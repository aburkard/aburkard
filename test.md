## Test: clickable grid cell options

### 1. bgcolor + nbsp

<table>
<tr><td bgcolor="#e0e0e0"><a href="#">&nbsp;&nbsp;&nbsp;</a></td><td bgcolor="#e74c3c"><a href="#">&nbsp;&nbsp;&nbsp;</a></td><td bgcolor="#3498db"><a href="#">&nbsp;&nbsp;&nbsp;</a></td><td bgcolor="#e0e0e0"><a href="#">&nbsp;&nbsp;&nbsp;</a></td></tr>
<tr><td bgcolor="#e0e0e0"><a href="#">&nbsp;&nbsp;&nbsp;</a></td><td bgcolor="#000000"><a href="#">&nbsp;&nbsp;&nbsp;</a></td><td bgcolor="#e0e0e0"><a href="#">&nbsp;&nbsp;&nbsp;</a></td><td bgcolor="#2ecc71"><a href="#">&nbsp;&nbsp;&nbsp;</a></td></tr>
</table>

### 2. bgcolor + unicode block (▇)

<table>
<tr><td bgcolor="#e0e0e0"><a href="#">▇</a></td><td bgcolor="#e74c3c"><a href="#">▇</a></td><td bgcolor="#3498db"><a href="#">▇</a></td><td bgcolor="#e0e0e0"><a href="#">▇</a></td></tr>
<tr><td bgcolor="#e0e0e0"><a href="#">▇</a></td><td bgcolor="#000000"><a href="#">▇</a></td><td bgcolor="#e0e0e0"><a href="#">▇</a></td><td bgcolor="#2ecc71"><a href="#">▇</a></td></tr>
</table>

### 3. bgcolor + thin space (multiple)

<table>
<tr><td bgcolor="#e0e0e0"><a href="#">&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;</a></td><td bgcolor="#e74c3c"><a href="#">&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;</a></td><td bgcolor="#3498db"><a href="#">&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;</a></td><td bgcolor="#e0e0e0"><a href="#">&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;</a></td></tr>
<tr><td bgcolor="#e0e0e0"><a href="#">&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;</a></td><td bgcolor="#000000"><a href="#">&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;</a></td><td bgcolor="#e0e0e0"><a href="#">&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;</a></td><td bgcolor="#2ecc71"><a href="#">&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;</a></td></tr>
</table>

### 4. emoji (original approach, in table)

<table>
<tr><td><a href="#">⬜</a></td><td><a href="#">🟥</a></td><td><a href="#">🟦</a></td><td><a href="#">⬜</a></td></tr>
<tr><td><a href="#">⬜</a></td><td><a href="#">⬛</a></td><td><a href="#">⬜</a></td><td><a href="#">🟩</a></td></tr>
</table>

### 5. bgcolor + em space

<table>
<tr><td bgcolor="#e0e0e0"><a href="#">&emsp;</a></td><td bgcolor="#e74c3c"><a href="#">&emsp;</a></td><td bgcolor="#3498db"><a href="#">&emsp;</a></td><td bgcolor="#e0e0e0"><a href="#">&emsp;</a></td></tr>
<tr><td bgcolor="#e0e0e0"><a href="#">&emsp;</a></td><td bgcolor="#000000"><a href="#">&emsp;</a></td><td bgcolor="#e0e0e0"><a href="#">&emsp;</a></td><td bgcolor="#2ecc71"><a href="#">&emsp;</a></td></tr>
</table>

### 6. bgcolor + dot (small visual, big click target)

<table>
<tr><td bgcolor="#e0e0e0"><a href="#">&nbsp;.&nbsp;</a></td><td bgcolor="#e74c3c"><a href="#">&nbsp;.&nbsp;</a></td><td bgcolor="#3498db"><a href="#">&nbsp;.&nbsp;</a></td><td bgcolor="#e0e0e0"><a href="#">&nbsp;.&nbsp;</a></td></tr>
<tr><td bgcolor="#e0e0e0"><a href="#">&nbsp;.&nbsp;</a></td><td bgcolor="#000000"><a href="#">&nbsp;.&nbsp;</a></td><td bgcolor="#e0e0e0"><a href="#">&nbsp;.&nbsp;</a></td><td bgcolor="#2ecc71"><a href="#">&nbsp;.&nbsp;</a></td></tr>
</table>

### 7. colored text matching bgcolor (invisible text)

<table>
<tr><td bgcolor="#e0e0e0"><a href="#"><font color="#e0e0e0">██</font></a></td><td bgcolor="#e74c3c"><a href="#"><font color="#e74c3c">██</font></a></td><td bgcolor="#3498db"><a href="#"><font color="#3498db">██</font></a></td><td bgcolor="#e0e0e0"><a href="#"><font color="#e0e0e0">██</font></a></td></tr>
<tr><td bgcolor="#e0e0e0"><a href="#"><font color="#e0e0e0">██</font></a></td><td bgcolor="#000000"><a href="#"><font color="#000000">██</font></a></td><td bgcolor="#e0e0e0"><a href="#"><font color="#e0e0e0">██</font></a></td><td bgcolor="#2ecc71"><a href="#"><font color="#2ecc71">██</font></a></td></tr>
</table>
