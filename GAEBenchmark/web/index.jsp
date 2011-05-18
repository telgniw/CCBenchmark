<%-- 
    Document   : index
    Created on : May 18, 2011, 7:50:26 PM
    Author     : Yi Huang (Celia)
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">

<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>GAEBenchmark Usage</title>
    </head>
    <body>
        <div>
            <table>
                <tr align="left"><th>URL</th><th>Parameters</th><th>Description</th></th>
                <tr><td>/newtask</td><td>url</td><td>"url" is a escaped string.</td></tr>
                <tr><td>/myblob/init</td><td>num, size</td><td>&nbsp;</td></tr>
                <tr><td>/myblob/upload</td><td>id</td><td>&nbsp;</td></tr>
                <tr><td>/myblob/download</td><td>id</td><td>&nbsp;</td></tr>
                <tr><td>/myblob/delete</td><td>N/A</td><td>Delete all data.</td></tr>
                <tr><td>/table/small/init</td><td>max, num, size, seed</td><td>&nbsp;</td></tr>
                <tr><td>/table/small/get</td><td>size, seed</td><td>&nbsp;</td></tr>
                <tr><td>/table/small/put</td><td>size, seed</td><td>&nbsp;</td></tr>
                <tr><td>/table/small/del</td><td>num, size, seed</td><td>&nbsp;</td></tr>
                <tr><td>/table/small/query</td><td>size, seed</td><td>&nbsp;</td></tr>
                <tr><td>/table/small/delete</td><td>N/A</td><td>Delete all data.</td></tr>
                <tr><td>/table/medium/init</td><td>max, num, size, seed</td><td>&nbsp;</td></tr>
                <tr><td>/table/medium/get</td><td>size, seed</td><td>&nbsp;</td></tr>
                <tr><td>/table/medium/put</td><td>size, seed</td><td>&nbsp;</td></tr>
                <tr><td>/table/medium/del</td><td>num, size, seed</td><td>&nbsp;</td></tr>
                <tr><td>/table/medium/query</td><td>size, seed</td><td>&nbsp;</td></tr>
                <tr><td>/table/medium/queryl</td><td>size, seed</td><td>Query by "Long".</td></tr>
                <tr><td>/table/medium/delete</td><td>N/A</td><td>Delete all data.</td></tr>
            </table>
        </div>
    </body>
</html>
