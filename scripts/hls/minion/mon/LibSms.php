<?php  

class LibSms
{
    const HTTP_AGENT = 'JecSpider Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)';

    public static function sendSms($mobiles, $params, $tpl_id,$config)
    {
        $random = rand();
        $time = time();

        //$config = ['sdkappid'=>$config['sdkappid'], 'appkey'=>$config['appkey']];
        $postData = ['tel'=>[], 'type'=>'0', 'params'=>$params, 'sig'=>'', 'sign'=>$config['sign'], 'ext'=>'', 'extend'=>'', 'tpl_id'=>$tpl_id, 'time'=>$time];

        if(is_array($mobiles))
        {
            foreach($mobiles as $mobile){
                $postData['tel'][] = ['nationcode'=>'86', 'mobile'=>$mobile];
            }

            $postData['sig'] = self::getSign($config['appkey'], $random, $time, implode(',', $mobiles));
            $serverUrl = "https://yun.tim.qq.com/v5/tlssmssvr/sendmultisms2?sdkappid={$config['sdkappid']}&random=".$random;
        }
        else
        {
            $postData['tel']['nationcode'] = '86';
            $postData['tel']['mobile'] = $mobiles;
            $postData['sig'] = self::getSign($config['appkey'], $random, $time, $mobiles);
            $serverUrl = "https://yun.tim.qq.com/v5/tlssmssvr/sendsms?sdkappid={$config['sdkappid']}&random=".$random;
        }


        $data = json_encode($postData);

        $result = self::fetch($serverUrl,
            array(
                CURLOPT_POST => true,
                CURLOPT_HTTPHEADER => array('Content-Type: application/json; charset=utf-8', 'Content-Length: ' . strlen($data)),
                CURLOPT_POSTFIELDS => $data,
            )
        );

        $result = json_decode($result, true); 
        return isset($result['result']) && $result['result'] == '0';
    }

    public static function fetch($url, $other_curl_opt = array(), &$http_code = 0, &$error = '')
    {
        $curl_opt = array(
            CURLOPT_URL => $url,
            CURLOPT_AUTOREFERER => true, //自动添加referer链接
            CURLOPT_RETURNTRANSFER => true, //true: curl_exec赋值方式，false：curl_exec直接输出结果
            CURLOPT_FOLLOWLOCATION => false, //自动跟踪301,302跳转
            CURLOPT_CONNECTTIMEOUT => 15, //秒
            CURLOPT_USERAGENT => self::HTTP_AGENT,
        );

        //curl传数组时，组建URL不正确，经常有些奇怪的问题导致无法正常请求
        if($other_curl_opt[CURLOPT_POSTFIELDS] && is_array($other_curl_opt[CURLOPT_POSTFIELDS]))
            $other_curl_opt[CURLOPT_POSTFIELDS] = http_build_query($other_curl_opt[CURLOPT_POSTFIELDS]);

        if($other_curl_opt)
            foreach ($other_curl_opt as $key => $val)
                $curl_opt[$key] = $val;

        $ch = curl_init();
        curl_setopt_array($ch, $curl_opt);
        $contents = curl_exec($ch);
        if ($contents === false) $error = curl_error($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        return $contents;
    }

    static public function getSign($appkey, $random, $time, $mobiles)
    {
        $str = 'appkey=' . $appkey . '&random=' . $random . '&time=' . $time . '&mobile=' . $mobiles;
        return self::SHA256Hex($str);
    }

    static public function SHA256Hex($str)
    {
        $re=hash('sha256', $str, true);
        return bin2hex($re);
    }
}


$config = [ 
        'tpl_id' => '367508',
        'title' => 'A8·H5',
        'sdkappid'=>'1400033617',
        'appkey'=>'0ecd07b95139d669c68f0638c6a78c73',
        'sign'=>'sh9130'
       ];
$number =[
			'13316291937','13580439512','13678913740','13760797097','18664621285','15627576701','13697979962',
        ];
$tplId = $config['tpl_id']; 
$params = isset($argv['1']) ? $argv['1'] : '暂无参数';  
$smss = new LibSms();
$smss->sendSms($number, array($params), $tplId, $config);
