# Path to create the directory
$tccPath = "C:\TCC"
$zipFilePath = "itc2.zip"
$exeFilePath = "C:\TCC\itc2\itc2.exe"
$blobUrl = "https://swbuildir2st.file.core.windows.net/win-dev-environment/itc2.zip?st=2023-12-10T08%3A26%3A35Z&se=2031-08-31T08%3A26%3A00Z&sp=r&sv=2022-11-02&sr=f&sig=v6tlCAeXz2%2FvwCFktPpYew4vyPyuJk%2B37K9zjxixBM4%3D"

Invoke-WebRequest -Uri $blobUrl -OutFile $zipFilePath
New-Item -ItemType Directory -Path $tccPath
Write-Host "Folder $tccPath created"

Expand-Archive -Path $zipFilePath -DestinationPath $tccPath
Write-Host "Extraced $zipFilePath into $tccPath"

Start-Process -FilePath $exeFilePath -ArgumentList "L4R:1.2.4"
Write-Host "Installed itc.exe"