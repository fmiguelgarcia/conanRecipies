#include <KF5/KArchive/KZip>
#include <QBuffer>
#include <QByteArray>

int main(int argc, char** argv )
{
	const QByteArray unCompressData = "This is uncompress data for testing";

	QByteArray compressData;
	QBuffer compressBuffer( &compressData);
	compressBuffer.open( QIODevice::WriteOnly);

	KZip zipper( &compressBuffer);
	zipper.open( QIODevice::WriteOnly); 
	zipper.writeFile( "test.txt", unCompressData);
	zipper.close();

	return 0;
}
