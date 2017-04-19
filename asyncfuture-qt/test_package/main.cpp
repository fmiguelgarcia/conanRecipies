#include <asyncFutureQt/asyncfuture.h>
using namespace AsyncFuture;

int main(int argc, char *argv[])
{
	auto defer = deferred<int>();
	auto future = defer.future();

	defer.complete(10);

	if( future.result() == 10)
		return 0;

	return -1;
}
