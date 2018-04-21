
def index(request):
    pie_runs = PieRun.objects.all()
    context = {
        'title': 'Pie Runs',
        'pie_runs': pie_runs
    }
    return render(request, 'pie_run/index.html', context)
