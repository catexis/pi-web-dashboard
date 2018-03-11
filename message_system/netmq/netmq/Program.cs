using NetMQ;
using NetMQ.Sockets;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace netmq
{
    class Program
    {
        static void Main(string[] args)
        {

            using (var server = new ResponseSocket())
            {
                server.Bind("tcp://*:5555");

                while (true)
                {
                    var message = server.ReceiveFrameString();

                    Console.WriteLine("Received {0}", message);

                    if(message == "powerpcoff")
                    { 
                        var psi = new ProcessStartInfo("shutdown", "/s /t 30");
                        psi.CreateNoWindow = true;
                        psi.UseShellExecute = false;
                        Process.Start(psi);
                        server.SendFrame("ok");
                    };

                    if (message == "tw")
                    {
                        Process.Start("C:\\Program Files (x86)\\TeamViewer\\TeamViewer.exe");
                        server.SendFrame("ok");
                    }
                    else  // В любом ином случае
                    {
                        Console.WriteLine("ok");
                        server.SendFrame("ok");
                    };

                }
            }

        }
    }
}
