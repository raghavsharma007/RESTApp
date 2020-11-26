<h1 class="code-line" data-line-start=0 data-line-end=1 ><a id="REST_API_0"></a>REST API</h1>
<p class="has-line-data" data-line-start="2" data-line-end="3">This APP has 4 endpoint URL:</p>
<ul>
<li class="has-line-data" data-line-start="3" data-line-end="4"><a href="http://localhost:8000/api/token/">http://localhost:8000/api/token/</a> (for obtaining JWT access token)</li>
<li class="has-line-data" data-line-start="4" data-line-end="5"><a href="http://localhost:8000/api/account/student/">http://localhost:8000/api/account/student/</a>&lt;email&gt;/ (to get student information)</li>
<li class="has-line-data" data-line-start="5" data-line-end="6"><a href="http://localhost:8000/api/account/access/">http://localhost:8000/api/account/access/</a> (for creation of Users by admin and students by teachers)</li>
<li class="has-line-data" data-line-start="6" data-line-end="8"><a href="http://localhost:8000/api/account/forgot_pass/">http://localhost:8000/api/account/forgot_pass/</a> (create new password using OTP)</li>
</ul>
<h1 class="code-line" data-line-start=8 data-line-end=9 ><a id="PostgreSQL_Used_8"></a>PostgreSQL Used</h1>
<p class="has-line-data" data-line-start="9" data-line-end="11">In this application a free cloud postgresql instance is created at <a href="http://www.elephantsql.com">www.elephantsql.com</a><br>
and configured in settings.</p>
<h1 class="code-line" data-line-start=12 data-line-end=13 ><a id="Obtain_JWT_Token_12"></a>Obtain JWT Token</h1>
<ul>
<li class="has-line-data" data-line-start="13" data-line-end="17">One test admin user is already created (email: <a href="mailto:admin@mail.com">admin@mail.com</a>, password: admin@123)<pre><code class="has-line-data" data-line-start="15" data-line-end="17" class="language-sh">POST http://localhost:<span class="hljs-number">8000</span>/api/token/
</code></pre>
</li>
<li class="has-line-data" data-line-start="17" data-line-end="25">set header and body<pre><code class="has-line-data" data-line-start="19" data-line-end="25" class="language-sh">Content-Type: application/json
body = {
    <span class="hljs-string">"email"</span>: <span class="hljs-string">"admin@mail.com"</span>,
    <span class="hljs-string">"password"</span>: <span class="hljs-string">"admin@123"</span>
}
</code></pre>
</li>
<li class="has-line-data" data-line-start="25" data-line-end="26">you will get refresh and access token. COPY access</li>
<li class="has-line-data" data-line-start="26" data-line-end="28">you can also use test student(<a href="mailto:email:student1@mail.com">email:student1@mail.com</a>, password:student1) or test teacher(<a href="mailto:email:teacher1@mail.com">email:teacher1@mail.com</a>, password:teacher1) instead of admin user above.</li>
</ul>
<h1 class="code-line" data-line-start=28 data-line-end=29 ><a id="create_and_get_users_28"></a>create and get users</h1>
<ul>
<li class="has-line-data" data-line-start="29" data-line-end="30">
<p class="has-line-data" data-line-start="29" data-line-end="30">Test admin user is already created (email: <a href="mailto:admin@mail.com">admin@mail.com</a>, password: admin@123) can create any User.</p>
</li>
<li class="has-line-data" data-line-start="30" data-line-end="34">
<p class="has-line-data" data-line-start="30" data-line-end="31">Test teacher(<a href="mailto:email:teacher1@mail.com">email:teacher1@mail.com</a>, password:teacher1) can only create users with group of student.</p>
<pre><code class="has-line-data" data-line-start="32" data-line-end="34" class="language-sh">POST http://localhost:<span class="hljs-number">8000</span>/api/account/access/
</code></pre>
</li>
<li class="has-line-data" data-line-start="34" data-line-end="35">
<p class="has-line-data" data-line-start="34" data-line-end="35">set authorization bearer token to access token copied before.</p>
</li>
<li class="has-line-data" data-line-start="35" data-line-end="45">
<p class="has-line-data" data-line-start="35" data-line-end="36">set header and body</p>
<pre><code class="has-line-data" data-line-start="37" data-line-end="45" class="language-sh">Content-Type: application/json
body = {
<span class="hljs-string">"email"</span>: <span class="hljs-string">"student4@mail.com"</span>,
<span class="hljs-string">"name"</span>: <span class="hljs-string">"student4"</span>,
<span class="hljs-string">"password"</span>: <span class="hljs-string">"student4"</span>,
<span class="hljs-string">"groups"</span>: [<span class="hljs-string">"student"</span>] or [<span class="hljs-string">"teacher"</span>] or [<span class="hljs-string">"admin"</span>]
}
</code></pre>
</li>
<li class="has-line-data" data-line-start="45" data-line-end="46">
<p class="has-line-data" data-line-start="45" data-line-end="46">Admin can create users with all three groups</p>
</li>
<li class="has-line-data" data-line-start="46" data-line-end="47">
<p class="has-line-data" data-line-start="46" data-line-end="47">test teacher(<a href="mailto:email:teacher1@mail.com">email:teacher1@mail.com</a>, password:teacher1) can only pass group: [“student”]</p>
</li>
<li class="has-line-data" data-line-start="47" data-line-end="49">
<p class="has-line-data" data-line-start="47" data-line-end="48">access token generated using test student(<a href="mailto:email:student1@mail.com">email:student1@mail.com</a>, password:student1) cannot create any user. The response in both with be Access denied with status code 401.</p>
</li>
<li class="has-line-data" data-line-start="49" data-line-end="53">
<p class="has-line-data" data-line-start="49" data-line-end="50">And to get User and students, GET</p>
<pre><code class="has-line-data" data-line-start="51" data-line-end="53" class="language-sh">GET http://localhost:<span class="hljs-number">8000</span>/api/account/access/
</code></pre>
</li>
<li class="has-line-data" data-line-start="53" data-line-end="54">
<p class="has-line-data" data-line-start="53" data-line-end="54">set authorization bearer token to access token copied before.</p>
</li>
<li class="has-line-data" data-line-start="54" data-line-end="58">
<p class="has-line-data" data-line-start="54" data-line-end="55">set header</p>
<pre><code class="has-line-data" data-line-start="56" data-line-end="58" class="language-sh">Content-Type: application/json
</code></pre>
</li>
<li class="has-line-data" data-line-start="58" data-line-end="59">
<p class="has-line-data" data-line-start="58" data-line-end="59">If access token is obtained with admin user credentials, all Users will be in response.</p>
</li>
<li class="has-line-data" data-line-start="59" data-line-end="60">
<p class="has-line-data" data-line-start="59" data-line-end="60">If Teacher credentials then only students will be in response.</p>
</li>
<li class="has-line-data" data-line-start="60" data-line-end="61">
<p class="has-line-data" data-line-start="60" data-line-end="61">Access token obtains using students credentials will return Access denied.</p>
</li>
</ul>
<h1 class="code-line" data-line-start=63 data-line-end=64 ><a id="Student_get_his_own_info_63"></a>Student get his own info</h1>
<ul>
<li class="has-line-data" data-line-start="64" data-line-end="68">One test admin user is already created (email: <a href="mailto:admin@mail.com">admin@mail.com</a>, password: admin@123)<pre><code class="has-line-data" data-line-start="66" data-line-end="68" class="language-sh">POST http://localhost:<span class="hljs-number">8000</span>/api/account/student/&lt;email&gt;/
</code></pre>
</li>
<li class="has-line-data" data-line-start="68" data-line-end="69">set authorization bearer token to access token copied before.pass your email in URL.</li>
<li class="has-line-data" data-line-start="69" data-line-end="73">set header and body<pre><code class="has-line-data" data-line-start="71" data-line-end="73" class="language-sh">Content-Type: application/json
</code></pre>
</li>
<li class="has-line-data" data-line-start="73" data-line-end="74">get access token using studentID and password, the response will be your info.</li>
<li class="has-line-data" data-line-start="74" data-line-end="76">If email passed in URL is different that the email used to get access token, response will be invalid access.</li>
</ul>
<h1 class="code-line" data-line-start=76 data-line-end=77 ><a id="Forgot_Password_76"></a>Forgot Password</h1>
<pre><code>    GET http://localhost:8000/api/account/forgot_pass/
</code></pre>
<ul>
<li class="has-line-data" data-line-start="78" data-line-end="86">set header and body<pre><code class="has-line-data" data-line-start="80" data-line-end="86" class="language-sh">Content-Type: application/json
body = {
    <span class="hljs-string">"email"</span>: <span class="hljs-string">"student1@mail.com"</span> 
    <span class="hljs-comment"># email of which you want to change pasword</span>
}
</code></pre>
</li>
<li class="has-line-data" data-line-start="86" data-line-end="87">you will get an OTP as response. COPY it.</li>
<li class="has-line-data" data-line-start="87" data-line-end="91">Now you have to make post request to change the password.<pre><code class="has-line-data" data-line-start="89" data-line-end="91" class="language-sh">POST http://localhost:<span class="hljs-number">8000</span>/api/account/forgot_pass/
</code></pre>
</li>
<li class="has-line-data" data-line-start="91" data-line-end="101">set header and body<pre><code class="has-line-data" data-line-start="93" data-line-end="101" class="language-sh">Content-Type: application/json
body = {
<span class="hljs-string">"email"</span>: <span class="hljs-string">"student1@mail.com"</span>, <span class="hljs-comment"># same email as used in GET</span>
<span class="hljs-string">"otp"</span>: <span class="hljs-number">689953</span>, <span class="hljs-comment"># otp received</span>
<span class="hljs-string">"password1"</span>: <span class="hljs-string">"changed1"</span>,
<span class="hljs-string">"password2"</span>: <span class="hljs-string">"changed1"</span>
}
</code></pre>
</li>
<li class="has-line-data" data-line-start="101" data-line-end="103">Check changed password to obtain JWT tokens.</li>
</ul>